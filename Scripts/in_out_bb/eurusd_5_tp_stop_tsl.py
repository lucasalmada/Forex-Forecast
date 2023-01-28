# Copyright 2022, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import time
import talib as ta
from out_in_bb import bb,bb_ema

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

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M5, 0, 300))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

   estr_1 = bb_ema(df,var_bb = 2,time_period = 20,pontos = 0.0004,rate_stop = 1,rate_tp = 1)
   

   acao = estr_1['acao'].values[0]
   close = estr_1['Close'].values[0]
   stop = estr_1['stop'].values[0]
   tp = estr_1['tp'].values[0]
   
   coment = 'stop_estr1'
    
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass
      
   '''coment = 'tsl_estr1'
   tp = 0.0 
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass'''
      
   
      
                                        

def verificar_2(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M5, 0, 300))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   estr_2 = bb(df,var_bb = 2.2,time_period = 30,pontos = 0.0005,rate_stop = 1,rate_tp = 1)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = 'stop_estr2'
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass
      
   '''coment = 'tsl_estr2'
   tp = 0.0
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass'''
                                        
while True: 
  data_e_hora_atuais = datetime.now()
  hour = int(str(data_e_hora_atuais.hour))
  second = int(str(data_e_hora_atuais.second))
  minute = int(str(data_e_hora_atuais.minute))
  if hour in [0,2,5,8,11,23]:
     if hour in [5,11,23,0,2]:
        if minute % 5 == 4 and second == 59:
           verificar_1(ativo = 'EURUSD.r') 
           time.sleep(1)
     if hour in [5,8,23,0]:
        if minute % 5 == 4 and second == 59:
           verificar_2(ativo = 'EURUSD.r')
           time.sleep(1)
  else:
     time.sleep(300)  

mt5.shutdown()
