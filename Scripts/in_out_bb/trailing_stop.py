# Copyright 2022, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import time
import talib as ta
mt5.initialize()


while True:
    #colonnes = ["ticket", "position", "symbol", "volume", "magic", "profit", "pip_diff", "tp", "sl","trade_size"]
    # Pega as posições em aberto
    liste = mt5.positions_get()
    for element in liste:
        '''element_pandas = pd.DataFrame([element.ticket, element.type, element.symbol, element.volume, element.magic,
                                        element.profit, element.price_current - element.price_open, element.tp,
                                        element.sl, mt5.symbol_info(element.symbol).trade_contract_size],
                                        index=colonnes).transpose()'''

        pip_diff = abs(element.sl - element.price_current)
        symbol = element.symbol
        position = element.type
        vol = element.volume
        price = element.price_open
        sl = element.sl
        ticket = element.ticket
        comment = element.comment
        
        pip_rate = 0.0004

        if comment[:3] == 'tsl':
            if pip_diff > pip_rate * 2:

                if position == 0:
                    request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "symbol": symbol,
                    "position": ticket,
                    "volume": vol,
                    "type": mt5.ORDER_TYPE_BUY,
                    "price": price,
                    "sl": sl + pip_rate + 0.00005,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                    "type_time": mt5.ORDER_TIME_GTC,
                    }
                    information = mt5.order_send(request)
                    print(information)

                else:
                    request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "symbol": symbol,
                    "position": ticket,
                    "volume": vol,
                    "type": mt5.ORDER_TYPE_SELL,
                    "price": price,
                    "sl": sl - pip_rate - 0.00005,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                    "type_time": mt5.ORDER_TIME_GTC,
                    }
                    information = mt5.order_send(request)
                    print(information)

        #summary = pd.concat((summary, element_pandas), axis=0)

    time.sleep(10)
                                        

                                        

mt5.shutdown()
