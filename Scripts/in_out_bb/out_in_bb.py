import pandas as pd
import MetaTrader5 as mt5
import talib as ta
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings("ignore")



def bb(df,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)

    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB_inicial'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 




    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1) else
                                    'sell' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1)
                                    
    lista = df['acao'].values
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

    df['acao'] = lista 


    lista = df['acao'].values
    lista_candles = [0] * len(df)
    lista_bb = df['pos_BB_inicial'].values
    tempo_lista =2
    for num, acao in enumerate(lista):
        #print(num,i)
        if acao == 'call':
            for i in range(tempo_lista):
                try:
                    if lista_bb[num+i+1] == 0:
                        lista_candles[num+i+1] = 'call'
                        break
                except:
                    pass
        if acao == 'sell':
            for i in range(tempo_lista):
                try:
                    if lista_bb[num+i+1] == 0:
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


    df_acao = df.tail(1)

    return df_acao
    
def bb_ema(df,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB_inicial'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 




    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)
                                    
    lista = df['acao'].values
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

    df['acao'] = lista 


    lista = df['acao'].values
    lista_candles = [0] * len(df)
    lista_bb = df['pos_BB_inicial'].values
    tempo_lista =2
    for num, acao in enumerate(lista):
        #print(num,i)
        if acao == 'call':
            for i in range(tempo_lista):
                try:
                    if lista_bb[num+i+1] == 0:
                        lista_candles[num+i+1] = 'call'
                        break
                except:
                    pass
        if acao == 'sell':
            for i in range(tempo_lista):
                try:
                    if lista_bb[num+i+1] == 0:
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


    df_acao = df.tail(1)

    return df_acao
    
    
def bb_candle(df,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)

    df['CDLENGULFING'] = ta.CDLENGULFING(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDL3INSIDE'] = ta.CDL3INSIDE(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLDOJI'] = ta.CDLDOJI(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLHAMMER'] = ta.CDLHAMMER(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLDARKCLOUDCOVER'] = ta.CDL3INSIDE(df['Open'],df['High'],df['Low'],df['Close'])  

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB_inicial'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 




    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1) else
                                    'sell' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1)
                                    
    lista = df['acao'].values
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

    df['acao'] = lista 


    lista = df['acao'].values
    lista_candles = [0] * len(df)
    lista_bb1 = df['CDLENGULFING'].values
    lista_bb2 = df['CDLENGULFING'].values
    lista_bb3 = df['CDLDARKCLOUDCOVER'].values
    lista_bb4 = df['CDLEVENINGSTAR'].values
    lista_bb5 = df['CDLMORNINGSTAR'].values
    lista_bb6 = df['CDL3INSIDE'].values
    tempo_lista =5
    for num, acao in enumerate(lista):
        #print(num,i)
        if acao == 'call':
            for i in range(tempo_lista):
                try:
                    if lista_bb1[num+i+1] == 100 or lista_bb5[num+i+1] == 100 or lista_bb6[num+i+1] == 100:
                        lista_candles[num+i] = 'call'
                        break
                except:
                    pass
        if acao == 'sell':
            for i in range(tempo_lista):
                try:
                    if lista_bb2[num+i+1] == -100 or lista_bb3[num+i+1] == -100 or lista_bb4[num+i+1] == -100 or lista_bb6[num+i+1] == -100:
                        lista_candles[num+i] = 'sell'
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


    df_acao = df.tail(1)

    return df_acao