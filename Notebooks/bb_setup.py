import pandas as pd
#import MetaTrader5 as mt5
import talib as ta
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings("ignore")

def main_indicators(df):

    df['MA_5'] = ta.SMA(df['Close'],timeperiod=5)
    df['MA_21'] = ta.SMA(df['Close'],timeperiod=21)
    df['SAR'] = ta.SAR(df['High'], df['Low'], acceleration=0, maximum=0)
    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['OBV'] = ta.OBV(df['Close'],df['Vol'])
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['fastk'], df['fastd'] = ta.STOCHF(df['High'], df['Low'], df['Close'], fastk_period=5, fastd_period=3, fastd_matype=0)
    df['RSI'] = ta.RSI(df['Close'],14)
    df['MOM'] = ta.MOM(df['Close'], timeperiod=10)
    df['TRIX'] = ta.TRIX(df['Close'], timeperiod=30)
    df['CCI'] = ta.CCI(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['dist_bb'] = df['BB_up'] - df['BB_low']
    df['dist_media'] = df['MA_5'] - df['MA_21']
    df['dist_media_abs'] = abs(df['MA_5'] - df['MA_21'])
    df['dist_price_media'] = df['MA_21'] - df['Close']
    df['dist_price_media'] = abs(df['MA_21'] - df['Close'])
    df['dist_RSI_70'] = df['RSI'] - 70
    df['dist_RSI_30'] = df['RSI'] - 30

    return df



def setup_1_old(df,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)

    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)

    percent_fechamento = 0.9

    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['verifica_tamanho']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['verifica_tamanho']) else 0 , axis = 1) 


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

    '''df['resultado_binario'] = df.apply(lambda x: 1 if (x['acao'] == 'call' and x['proximo_candle'] > 0) else 1 
                                                    if (x['acao'] == 'sell' and x['proximo_candle'] < 0) else 0, axis = 1)'''

    #pontos = 20
    #rate_stop é somado (multiplicador por tamanho de candle) em uma unidade de tamanho. rate 0.5 = stop 1.5 (somar 1)
    #rate_stop = 1
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

    df_acao = df[(df['acao'] != 0) & ((df['verifica_tamanho'] <=1))]

    return df_acao
    #df_acao['resultado_binario'].sum()/df_acao.shape[0]


def setup_2_old(df,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)

    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)

    percent_fechamento = 1

    df['acao'] = df.apply(lambda x: 'sell' if (x['pos_BB_inicial'] == -1) else
                                    'call' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1) 


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

    '''df['resultado_binario'] = df.apply(lambda x: 1 if (x['acao'] == 'call' and x['proximo_candle'] > 0) else 1 
                                                    if (x['acao'] == 'sell' and x['proximo_candle'] < 0) else 0, axis = 1)'''

    #pontos = 20
    #rate_stop é somado (multiplicador por tamanho de candle) em uma unidade de tamanho. rate 0.5 = stop 1.5 (somar 1)
    #rate_stop = 1
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
                    elif  df.loc[index + i,'Low'] <= row['tp']:
                        df.loc[index,'resultado_binario'] = 1
                        break
                    i+=1
                except:
                    df.loc[index,'resultado_binario'] = 0
                    break

    df_acao = df[(df['acao'] != 0) & ((df['verifica_tamanho'] <=1))]

    return df_acao
    #df_acao['resultado_binario'].sum()/df_acao.shape[0]


def setup_2(df,df_ticks,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2,timeframe = 5):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)

    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)

    percent_fechamento = 0

    df['acao'] = df.apply(lambda x: 'sell' if (x['pos_BB_inicial'] == -1 and x['verifica_tamanho'] >= percent_fechamento ) else
                                    'call' if (x['pos_BB_inicial'] == 1 and x['verifica_tamanho'] >= percent_fechamento) else 0 , axis = 1) 


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

    '''df['resultado_binario'] = df.apply(lambda x: 1 if (x['acao'] == 'call' and x['proximo_candle'] > 0) else 1 
                                                    if (x['acao'] == 'sell' and x['proximo_candle'] < 0) else 0, axis = 1)'''

    #pontos = 20
    #rate_stop é somado (multiplicador por tamanho de candle) em uma unidade de tamanho. rate 0.5 = stop 1.5 (somar 1)
    #rate_stop = 1
    df['stop'] = df.apply(lambda x: x['Close'] + (pontos * rate_stop)  if x['acao'] == 'sell' else 
    x['Close'] - (pontos * rate_stop) if x['acao'] == 'call' else 0, axis = 1)

    #rate_tp é somado em 0 unidades de tamanho. rate_tp 2 = tp 2  --Valor igual rate
    #rate_tp = 1.5
    df['tp'] = df.apply(lambda x: x['Close'] - rate_tp * pontos if x['acao'] == 'sell' else
                                            x['Close'] + rate_tp * pontos if x['acao'] == 'call' else 0, axis =1)

    
    df_acao = df[(df['acao'] != 0) & ((df['verifica_tamanho'] <=1))][['Data','Open','Close','acao','stop','tp']]

    timeframe = timeframe

    lista_result = []
    for index, row in df_acao.iterrows():
        data = row['Data']
        stop = row['stop']
        tp = row['tp']
        acao = row['acao']

        data = str(datetime.strptime(data, '%Y-%m-%d %H:%M:%S') + timedelta(minutes = timeframe))

        candles_10 = timeframe * 10 * 60

        if acao == 'call':

            media_lista = df_ticks[df_ticks['Data'] > data].iloc[:candles_10]['media']

            for valor_atual in media_lista:
                if valor_atual < stop:
                    df_acao.loc[index,'resultado_binario'] = 0
                    break
                elif valor_atual > tp:
                    df_acao.loc[index,'resultado_binario'] = 1
                    break
                else:
                    pass

        elif acao == 'sell':

            media_lista = df_ticks[df_ticks['Data'] > data].iloc[:candles_10]['media']

            for valor_atual in media_lista:
                if valor_atual > stop:
                    #lista_result.append(0)
                    df_acao.loc[index,'resultado_binario'] = 0
                    break
                elif valor_atual < tp:
                    df_acao.loc[index,'resultado_binario'] = 1
                    break
                else:
                    pass


    #df_acao['resultado_binario'] = lista_result

    return df_acao


def setup_1(df,df_ticks,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2,timeframe = 5):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)

    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)

    percent_fechamento = 0

    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['verifica_tamanho'] >= percent_fechamento ) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['verifica_tamanho'] >= percent_fechamento) else 0 , axis = 1) 


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

    '''df['resultado_binario'] = df.apply(lambda x: 1 if (x['acao'] == 'call' and x['proximo_candle'] > 0) else 1 
                                                    if (x['acao'] == 'sell' and x['proximo_candle'] < 0) else 0, axis = 1)'''

    #pontos = 20
    #rate_stop é somado (multiplicador por tamanho de candle) em uma unidade de tamanho. rate 0.5 = stop 1.5 (somar 1)
    #rate_stop = 1
    df['stop'] = df.apply(lambda x: x['Close'] + (pontos * rate_stop)  if x['acao'] == 'sell' else 
    x['Close'] - (pontos * rate_stop) if x['acao'] == 'call' else 0, axis = 1)

    #rate_tp é somado em 0 unidades de tamanho. rate_tp 2 = tp 2  --Valor igual rate
    #rate_tp = 1.5
    df['tp'] = df.apply(lambda x: x['Close'] - rate_tp * pontos if x['acao'] == 'sell' else
                                            x['Close'] + rate_tp * pontos if x['acao'] == 'call' else 0, axis =1)

    
    df_acao = df[(df['acao'] != 0) & ((df['verifica_tamanho'] <=1))][['Data','Open','Close','acao','stop','tp']]

    timeframe = timeframe

    lista_result = []
    for index, row in df_acao.iterrows():
        data = row['Data']
        stop = row['stop']
        tp = row['tp']
        acao = row['acao']

        data = str(datetime.strptime(data, '%Y-%m-%d %H:%M:%S') + timedelta(minutes = timeframe))

        candles_10 = timeframe * 10 * 60

        if acao == 'call':

            media_lista = df_ticks[df_ticks['Data'] > data].iloc[:candles_10]['media']

            for valor_atual in media_lista:
                if valor_atual < stop:
                    df_acao.loc[index,'resultado_binario'] = 0
                    break
                elif valor_atual > tp:
                    df_acao.loc[index,'resultado_binario'] = 1
                    break
                else:
                    pass

        elif acao == 'sell':

            media_lista = df_ticks[df_ticks['Data'] > data].iloc[:candles_10]['media']

            for valor_atual in media_lista:
                if valor_atual > stop:
                    #lista_result.append(0)
                    df_acao.loc[index,'resultado_binario'] = 0
                    break
                elif valor_atual < tp:
                    df_acao.loc[index,'resultado_binario'] = 1
                    break
                else:
                    pass


    #df_acao['resultado_binario'] = lista_result

    return df_acao