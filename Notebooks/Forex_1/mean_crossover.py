import pandas as pd
import MetaTrader5 as mt5
import talib as ta
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings("ignore")



def cross(df,ema1=30,ema2=50,pontos = 20,rate_stop = 1,rate_tp = 2,timeframe = 5):

    df['EMA_1'] = ta.EMA(df['Close'],timeperiod=ema1)
    df['EMA_2'] = ta.EMA(df['Close'],timeperiod=ema2)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=200)
    df['direcao_candle'] = (df['Close'] - df['Open']).apply(lambda x: 1 if x > 0 else 0)
    df['diff_media'] = (df['EMA_1'] - df['EMA_2']).apply(lambda x: 1 if x > 0 else -1)
    df['diff_media'] = df['diff_media'].diff()
    df['acao'] = df.apply(lambda x: 'call' if (x['diff_media'] == -2 and x['Close'] > x['EMA']) else 'sell' if (x['diff_media'] == 2 and x['Close'] < x['EMA']) else 0, axis = 1)



    lista = df['acao'].values
    lista_candles = df['direcao_candle']
    tempo_lista =3
    for num, acao in enumerate(lista):
        #print(num,i)
        if acao == 'call':
            for i in range(tempo_lista):
                try:
                    if lista_candles[num+i+1] == 0:
                        lista_candles[num+i+1] = 'call'
                        break
                except:
                    pass
        if acao == 'sell':
            for i in range(tempo_lista):
                try:
                    if lista_candles[num+i+1] == 1:
                        lista_candles[num+i+1] = 'sell'
                        break
                except:
                    pass
            

    df['acao'] = lista_candles

    df['stop'] = df.apply(lambda x: x['Close'] + (pontos * rate_stop)  if x['acao'] == 'sell' else 
        x['Close'] - (pontos * rate_stop) if x['acao'] == 'call' else 0, axis = 1)

    #rate_tp é somado em 0 unidades de tamanho. rate_tp 2 = tp 2  --Valor igual rate
    #rate_tp = 1.5
    df['tp'] = df.apply(lambda x: x['Close'] - rate_tp * pontos if x['acao'] == 'sell' else
                                            x['Close'] + rate_tp * pontos if x['acao'] == 'call' else 0, axis =1)

    for index, row in df.iterrows():
        if row['acao'] == 'call':
            i = 1
            while True:
                try:
                    if df.loc[index + i,'Low'] <= row['stop']:
                        df.loc[index,'resultado_binario'] = 0 
                        break
                    elif df.loc[index + i,'High'] >= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break
        elif row['acao'] == 'sell':
            i = 1
            while True:
                try:
                    if df.loc[index + i,'High'] >= row['stop']:
                        df.loc[index,'resultado_binario'] = 0
                        break
                    elif   df.loc[index + i,'Low'] <= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break



    df['acao'] = df['acao'].apply(lambda x: x if (x == 'call' or x == 'sell') else 0)

    df_acao = df[(df['acao'] != 0)]

    return df_acao


def cross_normal(df,ema1=30,ema2=50,pontos = 20,rate_stop = 1,rate_tp = 2,timeframe = 5):

    df['EMA_1'] = ta.EMA(df['Close'],timeperiod=ema1)
    df['EMA_2'] = ta.EMA(df['Close'],timeperiod=ema2)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['direcao_candle'] = (df['Close'] - df['Open']).apply(lambda x: 1 if x > 0 else 0)
    df['diff_media'] = (df['EMA_1'] - df['EMA_2']).apply(lambda x: 1 if x > 0 else -1)
    df['diff_media'] = df['diff_media'].diff()
    df['acao'] = df.apply(lambda x: 'sell' if (x['diff_media'] == -2 and x['Close'] < x['EMA']) else 'call' if (x['diff_media'] == 2 and x['Close'] > x['EMA']) else 0, axis = 1)



    lista = df['acao'].values
    lista_candles = df['direcao_candle']
    tempo_lista =3
    for num, acao in enumerate(lista):
        #print(num,i)
        if acao == 'call':
            for i in range(tempo_lista):
                try:
                    if lista_candles[num+i+1] == 0:
                        lista_candles[num+i+1] = 'call'
                        break
                except:
                    pass
        if acao == 'sell':
            for i in range(tempo_lista):
                try:
                    if lista_candles[num+i+1] == 1:
                        lista_candles[num+i+1] = 'sell'
                        break
                except:
                    pass
            

    df['acao'] = lista_candles

    df['stop'] = df.apply(lambda x: x['Close'] + (pontos * rate_stop)  if x['acao'] == 'sell' else 
        x['Close'] - (pontos * rate_stop) if x['acao'] == 'call' else 0, axis = 1)

    #rate_tp é somado em 0 unidades de tamanho. rate_tp 2 = tp 2  --Valor igual rate
    #rate_tp = 1.5
    df['tp'] = df.apply(lambda x: x['Close'] - rate_tp * pontos if x['acao'] == 'sell' else
                                            x['Close'] + rate_tp * pontos if x['acao'] == 'call' else 0, axis =1)

    for index, row in df.iterrows():
        if row['acao'] == 'call':
            i = 1
            while True:
                try:
                    if df.loc[index + i,'Low'] <= row['stop']:
                        df.loc[index,'resultado_binario'] = 0 
                        break
                    elif df.loc[index + i,'High'] >= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break
        elif row['acao'] == 'sell':
            i = 1
            while True:
                try:
                    if df.loc[index + i,'High'] >= row['stop']:
                        df.loc[index,'resultado_binario'] = 0
                        break
                    elif   df.loc[index + i,'Low'] <= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break



    df['acao'] = df['acao'].apply(lambda x: x if (x == 'call' or x == 'sell') else 0)

    df_acao = df[(df['acao'] != 0)]

    return df_acao