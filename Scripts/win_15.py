import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime,timedelta
import time
import talib as ta

#tz = pytz.timezone('America/Sao_Paulo')
ativo = 'WING23'
#ativos = ['EURUSD']


path = r'C:\Program Files\Clear Investimentos MT5 Terminal\terminal64.exe'

if not mt5.initialize(path = path):
    print("initialize() failed")
    mt5.shutdown()



def comprar(symbol,stop):
    point = mt5.symbol_info(symbol).point
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": stop,
        "tp": 0.0,
        "deviation": 20,
        "magic": 234000,
        "comment": "Compra-15M",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    print(result)

def vender(symbol,stop):
    point = mt5.symbol_info(symbol).point
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).bid,
        "sl": stop,
        "tp": 0.0,
        "deviation": 20,
        "magic": 234000,
        "comment": "Compra-5M",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    print(result)

def check_close(timestamp_abertura):
    tempo_espera = 75
    conserto_timestamp = -10800
    tempo_fechamento = timestamp_abertura + tempo_espera * 60
    agora_timestamp = int(datetime.now().timestamp()) + conserto_timestamp
    while tempo_fechamento > agora_timestamp:
        #print(str(datetime.fromtimestamp(tempo_fechamento)))
        agora_timestamp = int(datetime.now().timestamp()) + conserto_timestamp
        #print(str(datetime.fromtimestamp(agora_timestamp)))
        time.sleep(2)

    print('passou')

    result = mt5.Close(symbol = 'WING23')

    print(result)


def verificar(ativo):

    df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M15, 0, 200))
    df.columns = ['Data','Open','High','Low','Close','Vol','','']
    df['MA_9'] = ta.EMA(df['Close'], timeperiod = 9)
    df['MA_9_diff_value'] = df['MA_9'].diff(periods = 1)
    df['MA_9_tend'] = df['MA_9_diff_value'].apply(lambda x: 1 if x > 0 else -1)
    df['MA_9_tend_diff'] = df['MA_9_tend'].diff()
    df['MA_100'] = ta.SMA(df['Close'],timeperiod=100)
    df['tend'] = df.apply(lambda x: 1 if x['Close'] > x['MA_100'] else 0, axis = 1)

    df['acao'] = df.apply(lambda x: 'sell' if (x['MA_9_tend_diff'] == 2 and x['tend'] == 1) 
        else 'call' if  (x['MA_9_tend_diff'] == -2 and x['tend'] == 0)  else 0, axis =1)

    df['preco'] = df.apply(lambda x: x['Close'], axis =1)

    df['stop'] = df.apply(lambda x: x['High'] + (x['High'] - x['Low']) * 2 if x['acao']=='sell' else x['Low'] - (x['High'] - x['Low']) * 2 if x['acao'] == 'call' else 0, axis =1)



    ##Excluir seguidos
    lista = df['acao'].values

    tempo_lista = 10
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

    ultima_linha = df.iloc[-2:-1]
    preco_entrada = ultima_linha['preco'].values[0]
    stop = ultima_linha['stop'].values[0]
    acao = ultima_linha['acao'].values[0]

    if acao == 'call':
        comprar(ativo, stop)
    elif acao == 'sell':
        vender(ativo, stop)
    else:
        print('Sem operacao')


while True: 
    positions=mt5.positions_get()
    if positions:
        timestamp_abertura = positions[0].time
        check_close(timestamp_abertura)
    else:
        data_e_hora_atuais = datetime.now()
        hora_teste = str(data_e_hora_atuais.minute)
        time.sleep(1)
        if int(hora_teste) % 15 == 0:
            verificar(ativo)
            #print(str(data_e_hora_atuais))
            time.sleep(60)
            
