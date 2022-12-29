import pandas as pd
import talib as ta


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

def cal_result(x):
    if x['acao'] == 'call':
        if x['realizacao_simplista'] < x['stop']:
            resultado = x['stop'] - x['preco']
            return resultado
        else:
            resultado = x['realizacao_simplista'] - x['preco']
            return resultado
    if x['acao'] == 'sell':
        if x['realizacao_simplista'] > x['stop']:
            resultado = x['stop'] - x['preco']
            return resultado
        else:
            resultado = x['realizacao_simplista'] - x['preco']
            return resultado


def cal_result_2(x):
    if x['acao'] == 'call':
        if x['stop_real'] == 1:
            resultado = x['stop'] - x['preco']
            return resultado
        else:
            resultado = x['realizacao_simplista'] - x['preco']
            return resultado


def cal_result_new(x):
    if x['acao'] == 'sell':
        if x['stop_real'] == 1:
            resultado = x['preco'] - x['stop']
            return resultado
        else:
            resultado = x['preco'] - x['realizacao_simplista']
            return resultado
    elif x['acao'] == 'call':
        if x['stop_real'] == 1:
            resultado = x['stop'] - x['preco']
            return resultado
        else:
            resultado = x['realizacao_simplista'] - x['preco']
            return resultado

def cal_result_new_call(x):
    if x['acao'] == 'call':
        if x['stop_real'] == 1:
            resultado = x['stop'] - x['preco']
            return resultado
        else:
            resultado = x['realizacao_simplista'] - x['preco']
            return resultado


def Larry_simples_compra(df, tempo_fechar = -5, excluir_seguidos = True, acao = 'call'):

    df['MA_9'] = ta.EMA(df['Close'], timeperiod = 9)
    df['MA_9_diff_value'] = df['MA_9'].diff(periods = 1)
    df['MA_9_tend'] = df['MA_9_diff_value'].apply(lambda x: 1 if x > 0 else -1)
    df['MA_9_tend_diff'] = df['MA_9_tend'].diff()
    df['MA_100'] = ta.SMA(df['Close'],timeperiod=100)
    df['tend'] = df.apply(lambda x: 1 if x['Close'] > x['MA_100'] else 0, axis = 1)

    if acao == 'all':
        df['acao'] = df['MA_9_tend_diff'].apply(lambda x: 'sell' if x == 2 else 'call' if  x ==-2 else 0)
    elif acao == 'sell':
        df['acao'] = df['MA_9_tend_diff'].apply(lambda x: 'sell' if x == 2 else 0)
    else:
        df['acao'] = df['MA_9_tend_diff'].apply(lambda x: 'call' if  x ==-2 else 0)
        

    df['preco'] = df.apply(lambda x: x['Close'], axis =1)

    #Escolher o tamanho do stop
    df['stop'] = df.apply(lambda x: x['High'] + (x['High'] - x['Low'])  if x['acao']=='sell' else x['Low'] - (x['High'] - x['Low']) if x['acao'] == 'call' else 0, axis =1)
    #df['stop'] = df.apply(lambda x: x['High'] + 5  if x['acao']=='call' else x['High'] if x['acao'] == 'sell' else 0, axis =1)

    df['realizacao_simplista'] = df['Close'].shift(tempo_fechar)

    df = df.dropna()
    
    if excluir_seguidos:
        lista = df['acao'].values

        tempo_lista = abs(tempo_fechar)
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


    #Criar uma coluna onde seria um stop de verdade. 
    for index, row in df.iterrows():
        tempo = abs(tempo_fechar)
        if row['stop'] != 0:
            for i in range(tempo):
                try:
                    if df.loc[index + i + 1,'Low'] <= row['stop']: 
                            df.loc[index,'stop_real'] = 1
                except:
                    pass

    
    df = df.fillna(0)


    #Deixar apenas o DataFrame quando houve ação
    df_acao = df[df['acao'] != 0]



    df_acao['resultado_valor'] = df_acao.apply(cal_result_new_call, axis = 1)
    df_acao['resultado_binario'] = df_acao['resultado_valor'].apply(lambda x: 1 if x > 0 else 0)

    return df_acao


def Larry_completo_teste(df, tempo_fechar = -5, excluir_seguidos = True, acao = 'call', x_stop = 1):

    df['MA_9'] = ta.EMA(df['Close'], timeperiod = 9)
    df['MA_9_diff_value'] = df['MA_9'].diff(periods = 1)
    df['MA_9_tend'] = df['MA_9_diff_value'].apply(lambda x: 1 if x > 0 else -1)
    df['MA_9_tend_diff'] = df['MA_9_tend'].diff()
    df['MA_100'] = ta.SMA(df['Close'],timeperiod=100)
    df['tend'] = df.apply(lambda x: 1 if x['Close'] > x['MA_100'] else 0, axis = 1)

    if acao == 'all':
        df['acao'] = df.apply(lambda x: 'sell' if (x['MA_9_tend_diff'] == 2) 
        else 'call' if  (x['MA_9_tend_diff'] == -2)  else 0, axis =1)
    elif acao == 'sell':
        df['acao'] = df.apply(lambda x: 'sell' if (x['MA_9_tend_diff'] == 2 and x['tend'] == 1) else 0, axis = 1)
    elif acao == 'call':
        df['acao'] = df.apply(lambda x: 'call' if (x['MA_9_tend_diff'] == -2 and x['tend'] == 0) else 0, axis = 1)
        

    df['preco'] = df.apply(lambda x: x['Close'], axis =1)

    #Escolher o tamanho do stop
    df['stop'] = df.apply(lambda x: x['High'] + (x['High'] - x['Low']) * x_stop  if x['acao']=='sell' else x['Low'] - (x['High'] - x['Low']) * x_stop if x['acao'] == 'call' else 0, axis =1)
    #df['stop'] = df.apply(lambda x: x['High'] + 5  if x['acao']=='call' else x['High'] if x['acao'] == 'sell' else 0, axis =1)

    df['realizacao_simplista'] = df['Close'].shift(tempo_fechar)

    df = df.dropna()
    
    if excluir_seguidos:
        lista = df['acao'].values

        tempo_lista = abs(tempo_fechar)
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


    #Criar uma coluna onde seria um stop de verdade. 
    for index, row in df.iterrows():
        tempo = abs(tempo_fechar)
        if row['stop'] != 0 and row['acao'] == 'call':
            for i in range(tempo):
                try:
                    if df.loc[index + i + 1,'Low'] <= row['stop']: 
                            df.loc[index,'stop_real'] = 1
                except:
                    pass
        elif row['stop'] != 0 and row['acao'] == 'sell':
            for i in range(tempo):
                try:
                    if df.loc[index + i + 1,'High'] >= row['stop']: 
                            df.loc[index,'stop_real'] = 1
                except:
                    pass

    
    df = df.fillna(0)


    #Deixar apenas o DataFrame quando houve ação
    df_acao = df[df['acao'] != 0]



    df_acao['resultado_valor'] = df_acao.apply(cal_result_new, axis = 1)
    df_acao['resultado_binario'] = df_acao['resultado_valor'].apply(lambda x: 1 if x > 0 else 0)

    return df_acao


def Larry_completo(df, tempo_fechar = -5, excluir_seguidos = True, acao = 'call', x_stop = 1):

    df['MA_9'] = ta.EMA(df['Close'], timeperiod = 9)
    df['MA_9_diff_value'] = df['MA_9'].diff(periods = 1)
    df['MA_9_tend'] = df['MA_9_diff_value'].apply(lambda x: 1 if x > 0 else -1)
    df['MA_9_tend_diff'] = df['MA_9_tend'].diff()
    df['MA_100'] = ta.SMA(df['Close'],timeperiod=100)
    df['tend'] = df.apply(lambda x: 1 if x['Close'] > x['MA_100'] else 0, axis = 1)

    if acao == 'all':
        df['acao'] = df.apply(lambda x: 'sell' if (x['MA_9_tend_diff'] == 2 and x['tend'] == 1) 
        else 'call' if  (x['MA_9_tend_diff'] == -2 and x['tend'] == 0)  else 0, axis =1)
    elif acao == 'sell':
        df['acao'] = df.apply(lambda x: 'sell' if (x['MA_9_tend_diff'] == 2 and x['tend'] == 1) else 0, axis = 1)
    elif acao == 'call':
        df['acao'] = df.apply(lambda x: 'call' if (x['MA_9_tend_diff'] == -2 and x['tend'] == 0) else 0, axis = 1)
        

    df['preco'] = df.apply(lambda x: x['Close'], axis =1)

    #Escolher o tamanho do stop
    df['stop'] = df.apply(lambda x: x['High'] + (x['High'] - x['Low']) * x_stop  if x['acao']=='sell' else x['Low'] - (x['High'] - x['Low']) * x_stop if x['acao'] == 'call' else 0, axis =1)
    #df['stop'] = df.apply(lambda x: x['High'] + 5  if x['acao']=='call' else x['High'] if x['acao'] == 'sell' else 0, axis =1)

    df['realizacao_simplista'] = df['Close'].shift(tempo_fechar)

    df = df.dropna()
    
    if excluir_seguidos:
        lista = df['acao'].values

        tempo_lista = abs(tempo_fechar)
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


    #Criar uma coluna onde seria um stop de verdade. 
    for index, row in df.iterrows():
        tempo = abs(tempo_fechar)
        if row['stop'] != 0 and row['acao'] == 'call':
            for i in range(tempo):
                try:
                    if df.loc[index + i + 1,'Low'] <= row['stop']: 
                            df.loc[index,'stop_real'] = 1
                except:
                    pass
        elif row['stop'] != 0 and row['acao'] == 'sell':
            for i in range(tempo):
                try:
                    if df.loc[index + i + 1,'High'] >= row['stop']: 
                            df.loc[index,'stop_real'] = 1
                except:
                    pass

    
    df = df.fillna(0)


    #Deixar apenas o DataFrame quando houve ação
    df_acao = df[df['acao'] != 0]



    df_acao['resultado_valor'] = df_acao.apply(cal_result_new, axis = 1)
    df_acao['resultado_binario'] = df_acao['resultado_valor'].apply(lambda x: 1 if x > 0 else 0)

    return df_acao