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

    return df


def Larry_simples(df, tempo_fechar = -10):

    df['MA_9'] = ta.EMA(df['Close'], timeperiod = 9)
    df['MA_9_diff_value'] = df['MA_9'].diff(periods = 1)
    df['MA_9_tend'] = df['MA_9_diff_value'].apply(lambda x: 1 if x > 0 else -1)
    df['MA_9_tend_diff'] = df['MA_9_tend'].diff()

    df['acao'] = df['MA_9_tend_diff'].apply(lambda x: 'call' if x == 2 else 'sell' if  x ==-2 else 0)
    df['preco'] = df.apply(lambda x: x['High'] if x['acao']=='call' else x['Low'] if x['acao'] == 'sell' else 0, axis =1)
    df['stop'] = df.apply(lambda x: x['Low'] if x['acao']=='call' else x['High'] if x['acao'] == 'sell' else 0, axis =1)

    df['realizacao_simplista'] = df['Close'].shift(tempo_fechar)

    df = df.dropna()


    df_acao = df[df['acao'] != 0]



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

    df_acao['resultado_valor'] = df_acao.apply(cal_result, axis = 1)
    df_acao['resultado_binario'] = df_acao['resultado_valor'].apply(lambda x: 1 if x > 0 else 0)

    return df_acao