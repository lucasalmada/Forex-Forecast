import pandas as pd
import talib as ta
import warnings
warnings.filterwarnings("ignore")


def entrada_fechamento(x):
    if (x['cruza_media'] == 2 and x['fechamento_prox'] < x['Open']):
        return 'sell'
    elif (x['cruza_media'] == -2 and x['fechamento_prox'] > x['Open']):
        return 'call'

def entrada_min_max(x):
    if (x['cruza_media'] == 2 and x['minima_prox'] < x['Low']):
        return 'sell'
    elif (x['cruza_media'] == -2 and x['maxima_prox'] > x['High']):
        return 'call'

def trap_media(df,periodo_media = 20, rate_stop = 1, rate_tp = 3.5, limite_tamanho = 0):

    df['EMA_80'] = ta.EMA(df['Close'],timeperiod=periodo_media)
    df['tamanho_candle'] = abs(df['Open'] - df['Close'])
    df['pos_media'] = df.apply(lambda x: 1 if x['Close'] > x['EMA_80'] else -1, axis = 1)
    df['cruza_media'] = df['pos_media'].diff() #2 cruza pra cima ||| -2 cruza pra baixo || Candle que cruzou
    df['minima_prox'] =  df['Low'].shift(-1)
    df['maxima_prox'] =  df['High'].shift(-1)
    df['fechamento_prox'] = df['Close'].shift(-1)
    #verficar variações de mínimas e fechamentos
    #df['entrada_min_max'] = df.apply(lambda x: 1 if )


    df['entrada_fechamento'] = df.apply(entrada_fechamento, axis = 1)
    df['entrada_min_max'] = df.apply(entrada_min_max, axis = 1)
    df = df.fillna(0)

    metodo = 'entrada_min_max'
    #excluir seguidos

    lista = df[metodo].values

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

    df[metodo] = lista

    #rate_stop é somado (multiplicador por tamanho de candle) em uma unidade de tamanho. rate 0.5 = stop 1.5 (somar 1)
    rate_stop = rate_stop
    df['stop'] = df.apply(lambda x: x['Close'] + (x['tamanho_candle'] * rate_stop)  if x['cruza_media'] == 2 else 
    x['Close'] - (x['tamanho_candle'] * rate_stop) if x['cruza_media'] == -2 else 0, axis = 1)

    #rate_tp é somado em 0 unidades de tamanho. rate_tp 2 = tp 2  --Valor igual rate
    rate_tp = rate_tp
    df['tp'] = df.apply(lambda x: x['Open'] - rate_tp * x['tamanho_candle'] if x[metodo] == 'sell' else
                                            x['Open'] + rate_tp * x['tamanho_candle'] if x[metodo] == 'call' else 0, axis =1)


    for index, row in df.iterrows():
        if row['entrada_min_max'] == 'call':
            i = 1
            while True:
                try:
                    if df.loc[index + i,'High'] >= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    elif df.loc[index + i,'Low'] <= row['stop']:
                        df.loc[index,'resultado_binario'] = 0
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break
        elif row['entrada_min_max'] == 'sell':
            i = 1
            while True:
                try:
                    if df.loc[index + i,'Low'] <= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    elif df.loc[index + i,'High'] >= row['stop']:
                        df.loc[index,'resultado_binario'] = 0
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break

    df['acao'] = df[metodo]    

    '''df['Hora'] = df['Data'].apply(lambda x: x[11:])
    df['Hora_h'] = df['Hora'].apply(lambda x: x[:2])
    df['Hora_h'] = df['Hora_h'].apply(lambda x: int(x))
    df = df[df['Hora_h'] < 13]'''

    df_acao = df[(df[metodo] != 0) & (df['tamanho_candle'] > limite_tamanho)]

    return df_acao