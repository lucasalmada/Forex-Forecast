import sys
sys.path.append(r'./pricelevels')
from cluster import ZigZagClusterLevels
#from visualization.levels_with_zigzag import plot_with_pivots
#from pricelevels.cluster import RawPriceClusterLevels
import pandas as pd
import talib as ta
import warnings
warnings.filterwarnings("ignore")


def zig_zag(df,zig_zag_percent=0.2, merge_distance=None,
                                merge_percent=0.3, min_bars_between_peaks=10, peaks='All'):

    #Aqui entra o df do dia anterior

    zl = ZigZagClusterLevels(peak_percent_delta=zig_zag_percent, merge_distance=merge_distance,
                         merge_percent=merge_percent, min_bars_between_peaks= min_bars_between_peaks, 
                         peaks=peaks)

    #peaks =  Low,High,All
    zl.fit(df)

    levels = zl.levels

    return levels

def zig_zag_data(df,zig_zag_percent=0.3, merge_distance=None,
                         merge_percent=0.3, min_bars_between_peaks=10, peaks='All',
                         pontos = 0.0006,rate_tp = 1,plot = False,
                         rsi = [14,70,30]):

    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['RSI'] = ta.RSI(df['Close'],timeperiod=rsi[0])     
    df['MOM'] = ta.MOM(df['Close'],timeperiod=10)                  

 
    
    df['Data_d'] = df['Data'].apply(lambda x: x[:10])

    lista_data = df['Data_d'].unique()

    df_new = df[df['Data_d'] == lista_data[-2]]
    df_2 = df[df['Data_d'] == lista_data[-1]]

    levels = zig_zag(df_new,zig_zag_percent=zig_zag_percent, merge_distance=merge_distance,
                            merge_percent=merge_percent, min_bars_between_peaks=min_bars_between_peaks, 
                            peaks=peaks)

    lista_price = [x['price'] for x in levels]

    df_2['prox_linha'] = df_2['Close'].apply(lambda x: min(lista_price, key=lambda y:abs(y-x)))

    df_total = df_2.copy()


    #sup = 2, res = -2
    #Verificar Win rate pra Low, High e Close. Close é cruzamento, Low,High é encostar
    #estrategia 1 -> Cruzar no sup_res, entrar no candle que cruzou
    #estrategia 2 -> Cruzar no sup_res, entrar proximo candle revertendo 
    #estrategia 3 -> Toque no sup_res e proximo candle revertendo (inclusive pode ser o próprio candle) 

    '''df_total['sup_res'] = df_total[['Close','prox_linha']].apply(lambda x: 2 if (x['Close'] - x['prox_linha'] < 0.0004) and (x['Close'] - x['prox_linha'] > 0) 
                                                            else -2 if (x['Close'] - x['prox_linha'] < -0.0004) and (x['Close'] - x['prox_linha'] < 0) 
                                                            else 1 if (abs(x['Close'] - x['prox_linha']) > 0.0004)
                                                            else 0, axis = 1)'''
    df_total ['diff'] = df_total['Close'] - df_total['prox_linha']
    df_total['prox_linha_ant'] = df_total['prox_linha'].shift(1)

    df_total['sup'] = df_total[['Close','prox_linha','prox_linha_ant','RSI']].apply(lambda x: 1 if (x['Close'] - x['prox_linha'] > 0)
                                                                else -1 if (x['Close'] - x['prox_linha'] < 0) and
                                                                (x['prox_linha'] == x['prox_linha_ant']) and
                                                                x['RSI'] < rsi[2]
                                                                else 0,axis = 1)

    df_total['res'] = df_total[['Close','prox_linha','prox_linha_ant','RSI']].apply(lambda x: 2 if (x['Close'] - x['prox_linha'] < 0)
                                                                else -1 if (x['Close'] - x['prox_linha'] > 0) and
                                                                (x['prox_linha'] == x['prox_linha_ant']) and
                                                                x['RSI'] > rsi[1]
                                                                else 0,axis = 1)



    # 1--> Cruzou pra baixo, 2 --> Cruzou pra baixo 
    df_total['cruzamento_sup'] = df_total['sup'].diff().apply(lambda x: 1 if x == -2 else 0)
    df_total['cruzamento_res'] = df_total['res'].diff().apply(lambda x: 2 if x == -3 else 0)
    #df_total['cruzamento'] = df_total['sup_res'].diff().apply(lambda x: 1 if x == -2 else 2 if x == -3 else 0)

    df_total['acao'] = 0
    for index, row in df_total.iterrows():
        if row['cruzamento_sup'] == 1:
            df_total.loc[index,'acao'] = 'call'
        elif row['cruzamento_res'] == 2:
            df_total.loc[index,'acao'] = 'sell'

    #estrategia 1
    #df_total['acao'] = df_total['cruzamento'].apply(lambda x: 'call' if x == 1 else 'sell' if x == 2 else 0)

    #df_total['acao'] = df_total['cruzamento']

    lista = df_total['acao'].values
    tempo_lista =10
    for num, i in enumerate(lista):
        #print(num,i)
        if i != 0:
            for i in range(tempo_lista):
                try:
                    n_num = num + i + 1
                    lista[n_num] = 0
                except:
                    pass

    df_total['acao'] = lista
    
    df_total['stop'] = df_total.apply(lambda x: x['Close'] + (pontos)  if x['acao'] == 'sell' else 
            x['Close'] - (pontos) if x['acao'] == 'call' else 0, axis = 1)


    df_total['tp'] = df_total.apply(lambda x: x['Close'] - rate_tp * pontos if x['acao'] == 'sell' else
                                        x['Close'] + rate_tp * pontos if x['acao'] == 'call' else 0, axis =1)
    
    df_total = df_total.tail(1)

    return df_total