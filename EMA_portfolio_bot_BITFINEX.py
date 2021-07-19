#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:58:15 2021

@author: stevenwalgenbach
"""

import time
import requests
import json
import talib as ta
import pandas as pd
import numpy
import math

print("This is a test for GIT")

last_cross_tracker = 0
#Buy or Sell
last_cross_type = "NONE"

to_long_10_and_20 = []
to_short_10_and_20 = []

to_long_20_and_50 = []
to_short_20_and_50 = []

to_long_50_and_100 = []
to_short_50_and_100 = []


"""--------------------------------------------------------------------"""
def get_close_prices(instrument):
   close_price = []
   
   current_unix_ts = int(time.time()) 
   time_back = 86400*500
   after = current_unix_ts - time_back
   
   url = "https://api.cryptowat.ch/markets/Bitfinex/"+instrument+"USD/ohlc?after="+str(after)+"&periods=86400"
   request = requests.get(url)
   data = request.json()
   
   for d in data["result"]["86400"]:
    #print(d[4])
    close_price.append(float(d[4]))
    
   return close_price
"""--------------------------------------------------------------------"""
#EMA1 shorter than EMA2
def check_for_cross(EMA1_list,EMA2_list, instrument, EMA_length):
    global last_cross_type, last_cross_tracker, to_short_20_and_50, to_long_20_and_50, to_short_50_and_100, to_long_50_and_100
    EMA1 = 0
    EMA2 = 0 
    
    for i in range(len(EMA2_list)):
            
        EMA1 = EMA1_list[i]
        EMA2 = EMA2_list[i]
        
        
        
        if not math.isnan(EMA1) and not math.isnan(EMA2):
            
        
            #print(str(EMA1) + " : " + str(EMA2))
        
            if EMA1 > EMA2 and last_cross_type == "BULLISH":
                last_cross_tracker += 1
            elif EMA1 < EMA2 and last_cross_type == "BEARISH":
                last_cross_tracker += 1
            elif EMA1 > EMA2 and last_cross_type == "BEARISH" or last_cross_type == "NONE":
                last_cross_type = "BULLISH"
        
                last_cross_tracker = 0
            elif EMA1 < EMA2 and last_cross_type == "BULLISH" or last_cross_type == "NONE":
                last_cross_type = "BEARISH"
                last_cross_tracker = 0
    #print(EMA1)
    #print(EMA2)
                
        
    if last_cross_type in "BEARISH":
        if EMA_length in "MEDIUM_EMA":
            to_short_20_and_50.append(instrument)
        elif EMA_length in "LONG_EMA":
            to_short_50_and_100.append(instrument)
        elif EMA_length in "SHORT_EMA":
            to_short_10_and_20.append(instrument)
                    
    elif last_cross_type in "BULLISH":
        if EMA_length in "MEDIUM_EMA":
            to_long_20_and_50.append(instrument)
        elif EMA_length in "LONG_EMA":
            to_long_50_and_100.append(instrument)
        elif EMA_length in "SHORT_EMA":
            to_long_10_and_20.append(instrument)
        
    print(last_cross_type + "\nLast cross was: " + str(last_cross_tracker) + " candles ago\tDifference: " + str(abs(EMA1 - EMA2)))

"""--------------------------------------------------------------------"""
currencies = ["ETH", "BTC", "LTC", "ADA", "XRP", "EOS", "DOGE"]

for index in range(len(currencies)):
    print("-----------------------------------------------------------")
    
    instrument = currencies[index]
    
    closes = get_close_prices(instrument)
    current_close = closes[len(closes) - 1]
    #print(closes)
    df = numpy.array(closes, dtype=float)
    
    print("\n\nAnalysing: " + str(instrument) + " Price: " + str(current_close))
    print("EMA 10 and EMA 20:\n==========================")
    EMA_10 = ta.EMA(df, timeperiod=10)
    EMA_20 = ta.EMA(df, timeperiod=20)
    check_for_cross(EMA_10, EMA_20, instrument, "SHORT_EMA")
    print("EMA 20 and EMA 50:\n==========================")
    
    EMA_50 = ta.EMA(df, timeperiod=50)
    check_for_cross(EMA_20, EMA_50, instrument, "MEDIUM_EMA")
    print("\nEMA 50 and EMA 100:\n==========================")
    EMA_100 = ta.EMA(df, timeperiod=100)
    check_for_cross(EMA_50, EMA_100, instrument, "LONG_EMA")
    
    
    
    index += 1

"""
Need to add this for the different EMAs
"""
print("\n\n############# SUMMARY ################")
print("LONG:")
print("10 And 20 EMA:\n--------------------")
print(to_long_10_and_20)
print("20 And 50 EMA:\n--------------------")
print(to_long_20_and_50)
print("50 And 100 EMA:\n--------------------")
print(to_long_50_and_100)


print("\n\nSHORT:")
print("10 And 20 EMA:\n--------------------")
print(to_long_10_and_20)
print("20 And 50 EMA:\n--------------------")
print(to_short_20_and_50)
print("50 And 100 EMA:\n--------------------")
print(to_short_50_and_100)
    
    
    