# Copyright 2022, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import time
import talib as ta
from out_in_bb import bb_ema

mt5.initialize()


def comprar(ativo='EURUSD',stop=1,tp=1,coment=''):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ativo,
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(ativo).ask,
        "sl": stop,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": coment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)

def vender(ativo='EURUSD',stop=1,tp=1,coment=''):
    #point = mt5.symbol_info(ativo).point
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ativo,
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(ativo).bid,
        "sl": stop,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": coment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)


def verificar_1(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 300))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   estr_2 = bb_ema(df,var_bb = 2.2,time_period = 30,pontos = 0.0006,rate_stop = 1,rate_tp = 1)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = 'estr2_1M'
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass
      
                                        

def verificar_2(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 300))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   estr_2 = bb_ema(df,var_bb = 2.2,time_period = 30,pontos = 0.0002,rate_stop = 1,rate_tp = 1)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = 'estr2_1M'
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass
      
def verificar_3(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 300))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   estr_2 = bb_ema(df,var_bb = 2.4,time_period = 20,pontos = 0.0006,rate_stop = 1,rate_tp = 1)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = 'estr3_1M'
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass

                                        
while True: 
  data_e_hora_atuais = datetime.now()
  hour = int(str(data_e_hora_atuais.hour))
  second = int(str(data_e_hora_atuais.second))
  minute = int(str(data_e_hora_atuais.minute))
  if hour in [0,1,2,4,9,10,11,13,14,15,18,23]:
     if hour in [4,8,9,10,13,14,17,19,22]:
        if second == 59:
           verificar_1(ativo = 'EURUSD.r')
           time.sleep(1)    
     if hour in [18,23,0,1]:
        if second == 59:
           verificar_2(ativo = 'EURUSD.r')
           time.sleep(1)
     if hour in [9,11,13,15,23,2]:
        if second == 59:
           verificar_3(ativo = 'EURUSD.r')
           time.sleep(1)
  else:
     time.sleep(300)  

mt5.shutdown()
