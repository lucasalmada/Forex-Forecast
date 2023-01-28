# Copyright 2022, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import time
import talib as ta
from sup_res_1 import zig_zag_data

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

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 3000))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))
   
   zig_zag_percent = 0.2
   merge_percent = 0.1
   pontos = 0.0003
   rsi = [9,80,20]
   rate_tp = 2
   
   estr_1 = zig_zag_data(df,zig_zag_percent=zig_zag_percent, merge_distance=None,
                    merge_percent=merge_percent, min_bars_between_peaks=10, peaks='All',
                    pontos = pontos,rate_tp = rate_tp,rsi=rsi)
   

   acao = estr_1['acao'].values[0]
   close = estr_1['Close'].values[0]
   stop = estr_1['stop'].values[0]
   tp = estr_1['tp'].values[0]
   
   coment = '1M_estr1'
    
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass

      
   
                                        

def verificar_2(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 3000))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   zig_zag_percent = 0.3
   merge_percent = 0.1
   pontos = 0.0003
   rsi = [9,80,20]
   rate_tp = 1
   
   estr_2 = zig_zag_data(df,zig_zag_percent=zig_zag_percent, merge_distance=None,
                    merge_percent=merge_percent, min_bars_between_peaks=10, peaks='All',
                    pontos = pontos,rate_tp = rate_tp,rsi=rsi)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = '1M_estr2'
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass
      
def verificar_3(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 3000))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   zig_zag_percent = 0.3
   merge_percent = 0.1
   pontos = 0.0005
   rsi = [9,70,30]
   rate_tp = 1
   
   estr_2 = zig_zag_data(df,zig_zag_percent=zig_zag_percent, merge_distance=None,
                    merge_percent=merge_percent, min_bars_between_peaks=10, peaks='All',
                    pontos = pontos,rate_tp = rate_tp,rsi=rsi)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = '1M_estr3'
   
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      #print('Sem operacao')
      pass
      
def verificar_4(ativo = 'EURUSD'): 

   df = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 3000))
   df.columns = ['Data','Open','High','Low','Close','Vol','','']
   df['Data'] = pd.to_datetime(df['Data'], unit='s').apply(lambda x: str(x))

      
   zig_zag_percent = 0.3
   merge_percent = 0.1
   pontos = 0.0003
   rsi = [9,70,30]
   rate_tp = 2
   
   estr_2 = zig_zag_data(df,zig_zag_percent=zig_zag_percent, merge_distance=None,
                    merge_percent=merge_percent, min_bars_between_peaks=10, peaks='All',
                    pontos = pontos,rate_tp = rate_tp,rsi=rsi)
   

   acao = estr_2['acao'].values[0]
   close = estr_2['Close'].values[0]
   stop = estr_2['stop'].values[0]
   tp = estr_2['tp'].values[0]
   
   coment = '1M_estr4'
   
   
   if acao == 'call':
      comprar(ativo,stop,tp,coment)
   elif acao == 'sell':
      vender(ativo,stop,tp,coment)
   else:
      print('Sem operacao')
      pass

                                        
while True: 
  data_e_hora_atuais = datetime.now()
  hour = int(str(data_e_hora_atuais.hour))
  second = int(str(data_e_hora_atuais.second))
  minute = int(str(data_e_hora_atuais.minute))
  if hour in [1,2,3,5,7,8,9,10,11,13,15,19,21,22,23]:
     if hour in [1,3,7,8,19,21,22,23]:
        if second == 59:
           verificar_1(ativo = 'EURUSD.r') 
           time.sleep(1)
     if hour in [1,3,5,8,9,10,11,15]:
        if second == 59:
           verificar_2(ativo = 'EURUSD.r')
           time.sleep(1)
     if hour in [1,2,8,11,13,15,23]:
        if second == 59:
           verificar_3(ativo = 'EURUSD.r')
           time.sleep(1)
     if hour in [1,5,8,9,10,15,23]:
        if second == 59:
           verificar_4(ativo = 'EURUSD.r')
           time.sleep(1)
  else:
     time.sleep(300)  

mt5.shutdown()
