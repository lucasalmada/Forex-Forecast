import sys
sys.path.append(r'C:\Users\Usuário\Documents\Github\Forex-Forecast\pricelevels')
from cluster import ZigZagClusterLevels
from visualization.levels_with_zigzag import plot_with_pivots
from pricelevels.cluster import RawPriceClusterLevels
import numpy as np
import pandas as pd
import talib as ta
from backtesting import Strategy, Backtest
import MetaTrader5 as mt5
import plotly 
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def plot_zig_zag(df_train,df_test,zig_zag_percent=0.3, merge_distance=None,
                         merge_percent=0.3, min_bars_between_peaks=10, peaks='All',
                         width=800,height=600):

    zl = ZigZagClusterLevels(peak_percent_delta=zig_zag_percent, merge_distance=merge_distance,
                         merge_percent=merge_percent, min_bars_between_peaks= min_bars_between_peaks, 
                         peaks=peaks)

    #peaks =  Low,High,All
    zl.fit(df_train)

    fig = go.Figure(data=[go.Candlestick(x=df_train['Data'],
                open=df_train['Open'],
                high=df_train['High'],
                low=df_train['Low'],
                close=df_train['Close'],
                increasing_line_color= 'green', decreasing_line_color= 'red')])

    for price_j in zl.levels:
        price = price_j['price']
        fig.add_hline(y=price)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=200, label="200", step="minute", stepmode="backward"),
                dict(count=500, label="500", step="minute", stepmode="backward"),
                
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        autosize=False,
        width=width,
        height=height,)

    new = zl.levels

    fig.show()

    fig = go.Figure(data=[go.Candlestick(x=df_test['Data'],
                open=df_test['Open'],
                high=df_test['High'],
                low=df_test['Low'],
                close=df_test['Close'],
                increasing_line_color= 'green', decreasing_line_color= 'red')])

    for price_j in new:
        price = price_j['price']
        fig.add_hline(y=price)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=200, label="200", step="minute", stepmode="backward"),
                dict(count=500, label="500", step="minute", stepmode="backward"),
                
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        autosize=False,
        width=800,
        height=600)

    fig.show()


def plot_raw_level(df_train,df_test, merge_percent=0.2, use_maximums=True, bars_for_peak=31,
                            width = 800,height = 600):

    zl = RawPriceClusterLevels(None, merge_percent=merge_percent, use_maximums=use_maximums,
                                 bars_for_peak=bars_for_peak)

    #peaks =  Low,High,All
    zl.fit(df_train)

    fig = go.Figure(data=[go.Candlestick(x=df_train['Data'],
                open=df_train['Open'],
                high=df_train['High'],
                low=df_train['Low'],
                close=df_train['Close'],
                increasing_line_color= 'green', decreasing_line_color= 'red')])

    for price_j in zl.levels:
        price = price_j['price']
        fig.add_hline(y=price)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=200, label="200", step="minute", stepmode="backward"),
                dict(count=500, label="500", step="minute", stepmode="backward"),
                
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        autosize=False,
        width=width,
        height=height,)

    new = zl.levels

    fig.show()

    fig = go.Figure(data=[go.Candlestick(x=df_test['Data'],
                open=df_test['Open'],
                high=df_test['High'],
                low=df_test['Low'],
                close=df_test['Close'],
                increasing_line_color= 'green', decreasing_line_color= 'red')])

    for price_j in new:
        price = price_j['price']
        fig.add_hline(y=price)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=200, label="200", step="minute", stepmode="backward"),
                dict(count=500, label="500", step="minute", stepmode="backward"),
                
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        autosize=False,
        width=800,
        height=600)

    fig.show()


def zig_zag(df,zig_zag_percent=0.2, merge_distance=None,
                                merge_percent=0.3, min_bars_between_peaks=10, peaks='All'):

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
                         rsi=[9,70,30]):

    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['RSI'] = ta.RSI(df['Close'],timeperiod=rsi[0])     
    df['MOM'] = ta.MOM(df['Close'],timeperiod=10)                  

    
    df['Data_d'] = df['Data'].apply(lambda x: x[:10])

    lista_data = df['Data_d'].unique()
    


    df_total = None

    for num,data in enumerate(lista_data):

        try:
            df_new = df[df['Data_d'] == lista_data[num]]
            df_2 = df[df['Data_d'] == lista_data[num + 1]]

            levels = zig_zag(df_new,zig_zag_percent=zig_zag_percent, merge_distance=merge_distance,
                                    merge_percent=merge_percent, min_bars_between_peaks=min_bars_between_peaks, 
                                    peaks=peaks)

            lista_price = [x['price'] for x in levels]

            df_2['prox_linha'] = df_2['Close'].apply(lambda x: min(lista_price, key=lambda y:abs(y-x)))

            df_total = pd.concat([df_total,df_2])

        except:

            pass

    df_total['Data'] = pd.to_datetime(df_total['Data'])
    df_total = df_total.set_index('Data')


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

    df_total['signal'] = 0
    for index, row in df_total.iterrows():
        if row['cruzamento_sup'] == 1 and row['MOM'] < 0:
            df_total.loc[index,'signal'] = 1
        elif row['cruzamento_res'] == 2 and row['MOM'] > 0:
            df_total.loc[index,'signal'] = 2

    #estrategia 1
    #df_total['acao'] = df_total['cruzamento'].apply(lambda x: 'call' if x == 1 else 'sell' if x == 2 else 0)

    #df_total['signal'] = df_total['cruzamento']

    lista = df_total['signal'].values
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

    df_total['signal'] = lista


    def SIGNAL():
            return df_total.signal

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

    bt = Backtest(df_total, MyCandlesStrat, cash=100000000, commission=0,hedging=True)
    stats = bt.run()

    if plot:
        bt.plot()

    return stats


def zig_zag_2(df,zig_zag_percent=0.3, merge_distance=None,
                         merge_percent=0.3, min_bars_between_peaks=10, peaks='All',
                         pontos = 0.0006,rate_tp = 1,plot = False,
                         rsi=[9,70,30]):

    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['RSI'] = ta.RSI(df['Close'],timeperiod=rsi[0])     
    df['MOM'] = ta.MOM(df['Close'],timeperiod=10)    
               

    
    df['Data_d'] = df['Data'].apply(lambda x: x[:10])

    lista_data = df['Data_d'].unique()
    


    df_total = None

    for num,data in enumerate(lista_data):

        try:
            df_new = df[df['Data_d'] == lista_data[num]]
            df_2 = df[df['Data_d'] == lista_data[num + 1]]

            levels = zig_zag(df_new,zig_zag_percent=zig_zag_percent, merge_distance=merge_distance,
                                    merge_percent=merge_percent, min_bars_between_peaks=min_bars_between_peaks, 
                                    peaks=peaks)

            lista_price = [x['price'] for x in levels]

            df_2['prox_linha'] = df_2['Close'].apply(lambda x: min(lista_price, key=lambda y:abs(y-x)))

            df_total = pd.concat([df_total,df_2])

        except:

            pass

    df_total['dist_linha'] = df_total['Close'] -  df_total['prox_linha']  
    df_total['Data'] = pd.to_datetime(df_total['Data'])
    df_total = df_total.set_index('Data')


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
    #df_total['cruzamento_sup'] = df_total['sup'].diff().apply(lambda x: 1 if x == -2 else 0)
    #df_total['cruzamento_res'] = df_total['res'].diff().apply(lambda x: 2 if x == -3 else 0)

    df_total['cruzamento'] = df_total[['sup','res']].diff().apply(lambda x: 1 if x['sup'] == -2 
                                                else 2 if x['res'] == -3 else 0, axis = 1)

    '''df_total['signal'] = 0
    for index, row in df_total.iterrows():
        if row['cruzamento_sup'] == 1:
            df_total.loc[index,'signal'] = 1
        elif row['cruzamento_res'] == 2:
            df_total.loc[index,'signal'] = 2'''

    df_total['signal'] = 0
    lista_candles = [0] * len(df_total)
    lista_1 = df_total['cruzamento'].values
    #lista_2 = df['cruzamento_res'].values
    lista_3 = df_total['dist_linha'].values
    tempo_lista =5
    for num, acao in enumerate(lista_1):
        if acao == 1:
            for i in range(tempo_lista):
                try:
                    if lista_3[num+i+1] > 0:
                        lista_candles[num+i+1] = 1
                        break
                except:
                    pass
        if acao == 2:
            for i in range(tempo_lista):
                try:
                    if lista_3[num+i+1] < 0 :
                        lista_candles[num+i+1] = 2
                        break
                except:
                    pass

    df_total['signal'] = lista_candles

    #estrategia 1
    #df_total['acao'] = df_total['cruzamento'].apply(lambda x: 'call' if x == 1 else 'sell' if x == 2 else 0)

    #df_total['signal'] = df_total['cruzamento']

    lista = df_total['signal'].values
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

    df_total['signal'] = lista


    def SIGNAL():
            return df_total.signal

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

    bt = Backtest(df_total, MyCandlesStrat, cash=100000000, commission=0,hedging=True)
    stats = bt.run()

    if plot:
        bt.plot()

    return stats

def full_table(stats, pontos, rate_tp,rate_stop = 1,spread=0.00005,timeframe = 5
            ,zig_zag_percent=0.1,merge_percent=0.1):


    start = stats['Start'].date()
    end = stats['End'].date()

    n_trades = stats['# Trades']
    taxa_acerto = stats['Win Rate [%]']
    retorno = stats['Return [%]']

    acerto = n_trades * taxa_acerto/100
    erro = n_trades - acerto

    pontos_total = acerto * pontos * rate_tp - erro * pontos * rate_stop - spread * n_trades

    new = pd.DataFrame([[timeframe,pontos,zig_zag_percent,merge_percent,rate_tp,n_trades,taxa_acerto,pontos_total,retorno]])
    new.columns = ['Timeframe','pontos','zig_zag_percent','merge_percent','rate_tp','N_trades','Taxa_acerto','Pontos_total','Retorno']
    
    return new

def print_horario(stats,zig_zag_percent,merge_percent,pontos,rate_tp):


    df_trades = stats['_trades']
    #df_trades = df_trades.drop_duplicates('EntryTime')
    df_trades['Hora_h'] = df_trades['EntryTime'].apply(lambda x: x.hour)
    df_trades['resultado_binario'] = df_trades['ReturnPct'].apply(lambda x: 1 if x > 0 else 0)

    print(f'zig_zag_percent: {zig_zag_percent} -- merge_percent: {merge_percent} -- pontos: {pontos}--Rate_tp: {rate_tp}')
    df_new_hora = df_trades[['Hora_h','resultado_binario']]
    df_new_hora = df_trades.groupby(['Hora_h'],as_index=False).agg(qtd_operacoes=('resultado_binario', 'count'), taxa_acerto=('resultado_binario', 'mean'))

    #df_new_hora['pontos_liquido'] = df_new_hora.apply(calc_pontos, axis = 1)
    print(df_new_hora)





def zig_zag_data_estr_2(df,zig_zag_percent=0.3, merge_distance=None,
                         merge_percent=0.3, min_bars_between_peaks=10, peaks='All',
                         pontos = 0.0006,rate_tp = 1,plot = False):

    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    #df['RSI'] = ta.RSI(df['Close'],timeperiod=rsi[0])     
    df['MOM'] = ta.MOM(df['Close'],timeperiod=10)   
    df['CDLENGULFING'] = ta.CDLENGULFING(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDL3INSIDE'] = ta.CDL3INSIDE(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLDOJI'] = ta.CDLDOJI(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLHAMMER'] = ta.CDLHAMMER(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(df['Open'],df['High'],df['Low'],df['Close'])
    df['CDLDARKCLOUDCOVER'] = ta.CDL3INSIDE(df['Open'],df['High'],df['Low'],df['Close'])  
    df['direcao_candle'] = df['Close'] - df['Open']            

    
    df['Data_d'] = df['Data'].apply(lambda x: x[:10])

    lista_data = df['Data_d'].unique()


    df_total = None

    for num,data in enumerate(lista_data):

        try:
            '''df_new = df[df['Data_d'] == lista_data[num]]
            a1 = [lista_data[num-1]]
            a2 = [lista_data[num-2]]
            df_2 = df[df['Data_d'].isin(a1 + a2)]'''

            df_new = df[df['Data_d'] == lista_data[num]]
            df_2 = df[df['Data_d'] == lista_data[num + 1]]

            levels = zig_zag(df_new,zig_zag_percent=zig_zag_percent, merge_distance=merge_distance,
                                    merge_percent=merge_percent, min_bars_between_peaks=min_bars_between_peaks, 
                                    peaks=peaks)

            lista_price = [x['price'] for x in levels]

            df_2['prox_linha'] = df_2['Close'].apply(lambda x: min(lista_price, key=lambda y:abs(y-x)))

            df_total = pd.concat([df_total,df_2])

        except:

            pass

    df_total['Data'] = pd.to_datetime(df_total['Data'])
    df_total = df_total.set_index('Data')


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

    df_total['sup'] = df_total[['Close','prox_linha','prox_linha_ant']].apply(lambda x: 1 if (x['Close'] - x['prox_linha'] > 0)
                                                                else -1 if (x['Close'] - x['prox_linha'] < 0) and
                                                                (x['prox_linha'] == x['prox_linha_ant'])
                                                                else 0,axis = 1)

    df_total['res'] = df_total[['Close','prox_linha','prox_linha_ant']].apply(lambda x: 2 if (x['Close'] - x['prox_linha'] < 0)
                                                                else -1 if (x['Close'] - x['prox_linha'] > 0) and
                                                                (x['prox_linha'] == x['prox_linha_ant']) 
                                                                else 0,axis = 1)



    # 1--> Cruzou pra baixo, 2 --> Cruzou pra baixo 
    df_total['cruzamento_sup'] = df_total['sup'].diff().apply(lambda x: 1 if x == -2 else 0)
    df_total['cruzamento_res'] = df_total['res'].diff().apply(lambda x: 2 if x == -3 else 0)
    #df_total['cruzamento'] = df_total['sup_res'].diff().apply(lambda x: 1 if x == -2 else 2 if x == -3 else 0)

    df_total['signal'] = 0
    for index, row in df_total.iterrows():
        if row['cruzamento_sup'] == 1:
            df_total.loc[index,'signal'] = 'call'
        elif row['cruzamento_res'] == 2:
            df_total.loc[index,'signal'] = 'sell'

    #estrategia 1
    #df_total['acao'] = df_total['cruzamento'].apply(lambda x: 'call' if x == 1 else 'sell' if x == 2 else 0)

    #df_total['signal'] = df_total['cruzamento']

    lista = df_total['signal'].values
    tempo_lista =15
    for num, i in enumerate(lista):
        #print(num,i)
        if i != 0:
            for i in range(tempo_lista):
                try:
                    n_num = num + i + 1
                    lista[n_num] = 0
                except:
                    pass

    df_total['signal'] = lista


    lista = df_total['signal'].values
    lista_candles = [0] * len(df_total)
    lista_bb1 = df_total['CDLENGULFING'].values
    lista_bb2 = df_total['CDLENGULFING'].values
    lista_bb3 = df_total['CDLDARKCLOUDCOVER'].values
    lista_bb4 = df_total['CDLEVENINGSTAR'].values
    lista_bb5 = df_total['CDLMORNINGSTAR'].values
    lista_bb6 = df_total['CDL3INSIDE'].values
    direcao = df_total['direcao_candle'].values
    tempo_lista =1
    for num, acao in enumerate(lista):
        #print(num,i)
        if acao == 'call':
            for i in range(tempo_lista):
                try:
                    if lista_bb1[num+i+1] == 100  or lista_bb6[num+i+1] == 100:
                    #if direcao[num+i+1] < 0:
                        lista_candles[num+i+1] = 'sell'
                    break
                except:
                    pass
        if acao == 'sell':
            for i in range(tempo_lista):
                try:
                    if lista_bb2[num+i+1] == -100 or lista_bb3[num+i+1] == -100  or lista_bb6[num+i+1] == -100:
                    #if direcao[num+i+1] > 0:
                        lista_candles[num+i+1] = 'call'
                        break
                except:
                    pass
            

    df_total['signal'] = lista_candles 
    df_total['signal'] = df_total['signal'].apply(lambda x: 1 if x == 'call' else 2 if x=='sell' else 0)


    def SIGNAL():
            return df_total.signal

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

    bt = Backtest(df_total, MyCandlesStrat, cash=100000000, commission=0,hedging=True)
    stats = bt.run()

    if plot:
        bt.plot()

    return stats

def zig_zag_100(df,zig_zag_percent=0.3, merge_distance=None,
                         merge_percent=0.3, min_bars_between_peaks=10, peaks='All',
                         pontos = 0.0006,rate_tp = 1,plot = False,
                         rsi=[9,70,30], n_cluster = 100):

    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['RSI'] = ta.RSI(df['Close'],timeperiod=rsi[0])     
    df['MOM'] = ta.MOM(df['Close'],timeperiod=10)                  

    
    df['Data_d'] = df['Data'].apply(lambda x: x[:10])

    lista_data = df['Data_d'].unique()
    


    df_total = None

    n_cluster = n_cluster
    for num in range(int(len(df)/n_cluster) - 1):

        try:
            df_new = df.iloc[n_cluster * num:n_cluster * (num + 1)]
            df_2 = df.iloc[n_cluster * (num + 1):n_cluster * (num + 2)]
  

            levels = zig_zag(df_new,zig_zag_percent=zig_zag_percent, merge_distance=merge_distance,
                                    merge_percent=merge_percent, min_bars_between_peaks=min_bars_between_peaks, 
                                    peaks=peaks)

            lista_price = [x['price'] for x in levels]

            df_2['prox_linha'] = df_2['Close'].apply(lambda x: min(lista_price, key=lambda y:abs(y-x)))

            df_total = pd.concat([df_total,df_2])

        except:

            pass

    df_total['Data'] = pd.to_datetime(df_total['Data'])
    df_total = df_total.set_index('Data')


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

    df_total['signal'] = 0
    for index, row in df_total.iterrows():
        if row['cruzamento_sup'] == 1:
            df_total.loc[index,'signal'] = 1
        elif row['cruzamento_res'] == 2:
            df_total.loc[index,'signal'] = 2

    #estrategia 1
    #df_total['acao'] = df_total['cruzamento'].apply(lambda x: 'call' if x == 1 else 'sell' if x == 2 else 0)

    #df_total['signal'] = df_total['cruzamento']

    lista = df_total['signal'].values
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

    df_total['signal'] = lista


    def SIGNAL():
            return df_total.signal

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

    bt = Backtest(df_total, MyCandlesStrat, cash=100000000, commission=0,hedging=True)
    stats = bt.run()

    if plot:
        bt.plot()

    return stats

def zig_zag_tsl(df,zig_zag_percent=0.3, merge_distance=None,
                         merge_percent=0.3, min_bars_between_peaks=10, peaks='All',
                         pontos = 0.0006,rate_tp = 1,plot = False,
                         rsi=[9,70,30]):

    df['EMA'] = ta.EMA(df['Close'],timeperiod=250)
    df['RSI'] = ta.RSI(df['Close'],timeperiod=rsi[0])     
    df['MOM'] = ta.MOM(df['Close'],timeperiod=10)                  

    
    df['Data_d'] = df['Data'].apply(lambda x: x[:10])

    lista_data = df['Data_d'].unique()


    df_total = None

    for num,data in enumerate(lista_data):

        try:
            df_new = df[df['Data_d'] == lista_data[num]]
            df_2 = df[df['Data_d'] == lista_data[num + 1]]

            levels = zig_zag(df_new,zig_zag_percent=zig_zag_percent, merge_distance=merge_distance,
                                    merge_percent=merge_percent, min_bars_between_peaks=min_bars_between_peaks, 
                                    peaks=peaks)

            lista_price = [x['price'] for x in levels]

            df_2['prox_linha'] = df_2['Close'].apply(lambda x: min(lista_price, key=lambda y:abs(y-x)))

            df_total = pd.concat([df_total,df_2])

        except:

            pass

    df_total['Data'] = pd.to_datetime(df_total['Data'])
    df_total = df_total.set_index('Data')


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

    df_total['signal'] = 0
    for index, row in df_total.iterrows():
        if row['cruzamento_sup'] == 1:
            df_total.loc[index,'signal'] = 1
        elif row['cruzamento_res'] == 2:
            df_total.loc[index,'signal'] = 2

    #estrategia 1
    #df_total['acao'] = df_total['cruzamento'].apply(lambda x: 'call' if x == 1 else 'sell' if x == 2 else 0)

    #df_total['signal'] = df_total['cruzamento']

    lista = df_total['signal'].values
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

    df_total['signal'] = lista


    def SIGNAL():
            return df_total.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next()
            sltr = 0.0004
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

    bt = Backtest(df_total, MyCandlesStrat, cash=100000000, commission=0,hedging=True)
    stats = bt.run()

    if plot:
        bt.plot()

    return stats
