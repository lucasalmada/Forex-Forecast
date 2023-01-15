import pandas as pd
#import MetaTrader5 as mt5
import talib as ta
from datetime import datetime,timedelta
from backtesting import Strategy, Backtest
import numpy as np
import warnings
warnings.filterwarnings("ignore")



def setup_stop_tp(df,timeperiod=20,var_bb=2,pontos = 100,rate_tp =2,EMA =True):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=timeperiod, nbdevup=var_bb, nbdevdn=var_bb, matype=0)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=200)
    #df['RSI'] = ta.RSI(df['Close'],14)
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    '''df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)'''

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB_inicial'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    
    ''' df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)
'''


    '''df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1) else
                                    'sell' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1)
'''
    '''df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)'''
    

    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)

    '''df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['macdhist'] > -50) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['macdhist'] < 50) else 0 , axis = 1)'''
    if EMA:
        df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)
    else:
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
            

    df['signal'] = lista_candles 
    df['signal'] = df['signal'].apply(lambda x: 1 if x == 'call' else 2 if x=='sell' else 0)



    df['Hora'] = df['Data'].apply(lambda x: x[11:])
    df['Hora_h'] = df['Hora'].apply(lambda x: x[:2])

    lista_horas = df['Hora_h'].values
    lista_signal = df['signal'].values

    for num,value in enumerate(lista_horas):
        if value in ['18']:
            lista_signal[num] = 0

    df['signal'] = lista_signal 

    df['Data'] = pd.to_datetime(df['Data'])
    df = df.set_index('Data')

    def SIGNAL():
        return df.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next() 
            sl = pontos
            tp = pontos * rate_tp
            if self.signal1==1:
                sl1 = self.data.Close[-1] - sl
                tp1 = self.data.Close[-1] + tp
                self.buy(sl=sl1, tp=tp1)
            elif self.signal1==2:
                sl1 = self.data.Close[-1] + sl
                tp1 = self.data.Close[-1] - tp
                self.sell(sl=sl1, tp=tp1)

    bt = Backtest(df, MyCandlesStrat, cash=100000000, commission=0)
    bt.run()
    #bt.plot()
    return bt

def setup_tsl(df,timeperiod=20,var_bb=2,pontos = 20,rate_stop = 1,rate_tp = 2,timeframe = 5, EMA = True):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=timeperiod, nbdevup=var_bb, nbdevdn=var_bb, matype=0)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    #df['RSI'] = ta.RSI(df['Close'],14)
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    '''df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)'''

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB_inicial'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    
    ''' df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)
'''


    '''df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1) else
                                    'sell' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1)
'''
    '''df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)'''
    

    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)

    '''df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['macdhist'] > -50) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['macdhist'] < 50) else 0 , axis = 1)'''
    
    if EMA:
        df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)
    else:
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
            

    df['signal'] = lista_candles 
    df['signal'] = df['signal'].apply(lambda x: 1 if x == 'call' else 2 if x=='sell' else 0)

    df['Hora'] = df['Data'].apply(lambda x: x[11:])
    df['Hora_h'] = df['Hora'].apply(lambda x: x[:2])

    lista_horas = df['Hora_h'].values
    lista_signal = df['signal'].values

    for num,value in enumerate(lista_horas):
        if value in ['18']:
            lista_signal[num] = 0

    df['signal'] = lista_signal

    df['Data'] = pd.to_datetime(df['Data'])
    df = df.set_index('Data')

    def SIGNAL():
        return df.signal

    class MyCandlesStrat(Strategy):
        sltr = 0.0010
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next()
            sltr = self.sltr
            for trade in self.trades: 
                if trade.is_long: 
                    trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - sltr)
                else:
                    trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + sltr) 

            if self.signal1==1: # trades number change!
                sl1 = self.data.Close[-1] - sltr
                self.buy(sl=sl1)
            elif self.signal1==2: # trades number change!
                sl1 = self.data.Close[-1] + sltr
                self.sell(sl=sl1)

    bt = Backtest(df, MyCandlesStrat, cash=100000000, commission=0)
    bt.run()
    #bt.plot()
    return bt




def setup_2(df,timeperiod=20,var_bb=2,pontos = 20,rate_stop = 1,rate_tp = 2,timeframe = 5):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=timeperiod, nbdevup=var_bb, nbdevdn=var_bb, matype=0)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB_inicial'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)



    '''df['acao'] = df.apply(lambda x: 'sell' if (x['pos_BB_inicial'] == -1) else
                                    'call' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1)'''

    '''df['acao'] = df.apply(lambda x: 'sell' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'call' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)
'''
    df['acao'] = df.apply(lambda x: 'sell' if (x['pos_BB_inicial'] == -1 and x['tamanho_corpo'] < 20) else
                                    'call' if (x['pos_BB_inicial'] == 1 and x['tamanho_corpo'] < 20) else 0 , axis = 1)

    '''df['acao'] = df.apply(lambda x: 'sell' if (x['pos_BB_inicial'] == -1 and x['macdhist'] > -20 and x['Close'] < x['EMA']) else
                                    'call' if (x['pos_BB_inicial'] == 1 and x['macdhist'] < 20 and x['Close'] > x['EMA']) else 0 , axis = 1)
'''

    lista = df['acao'].values
    lista_candles = [0] * len(df)
    lista_bb = df['pos_BB_inicial'].values
    tempo_lista =1
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

    df_acao = df[(df['acao'] != 0)]

    return df_acao

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

    '''df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)
'''
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

    df_acao = df[(df['acao'] != 0)]

    return df_acao


def setup_1_old(df,var_bb = 2,time_period = 20,pontos = 20,rate_stop = 1,rate_tp = 2):

    df['BB_up'],df['BB_mid'],df['BB_low'] = ta.BBANDS(df['Close'], timeperiod=time_period, nbdevup=var_bb, nbdevdn=var_bb, matype=0)
    df['EMA'] = ta.EMA(df['Close'],timeperiod=200)
    df['tamanho_corpo'] = abs(df['Open'] - df['Close'])
    df['tamanho_pra_baixo'] = abs(df['Open'] - df['Low'])
    df['tamanho_abaixo'] = abs(df['Close'] - df['Low'])
    df['tamanho_pra_cima'] = abs(df['Open'] - df['High'])
    df['tamanho_acima'] = abs(df['High'] - df['Close'])
    df['proximo_candle'] = df['Close'].shift(-1) - df['Open'].shift(-1)

    df['pos_BB_inicial'] = df.apply(lambda x: 1 if x['Close'] > x['BB_up'] else -1 if x['Close'] < x['BB_low'] else 0, axis = 1)
    #df['pos_BB'] = df['pos_BB_inicial'].diff()

    #pos_BB = -2 cruzou pra BB_low pra baixo // pos_BB = 2 cruzou BB_high pra cima // 

    '''df['verifica_tamanho'] = df.apply(lambda x: x['tamanho_corpo']/(x['tamanho_pra_baixo'] + 1e-4) if x['pos_BB_inicial'] == -1 else
                                        x['tamanho_corpo']/(x['tamanho_pra_cima'] + 1e-4) if x['pos_BB_inicial'] == 1 else 0, axis = 1)
'''
    percent_fechamento = 1

    df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1 and x['Close'] > x['EMA']) else
                                    'sell' if (x['pos_BB_inicial'] == 1 and x['Close'] < x['EMA']) else 0 , axis = 1)

    ''' df['acao'] = df.apply(lambda x: 'call' if (x['pos_BB_inicial'] == -1) else
                                    'sell' if (x['pos_BB_inicial'] == 1) else 0 , axis = 1) '''


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

    df_acao = df[(df['acao'] != 0)]

    return df_acao