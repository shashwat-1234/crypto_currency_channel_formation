from __future__ import print_function

import pandas as pd
import requests
import json
import time
from datetime import datetime

import sys

import gate_api
from gate_api.exceptions import ApiException, GateApiException

import plotly.graph_objs as go
from plotly.offline import plot

#functions to convert time 
def UnixToNatural(t):
    return datetime.fromtimestamp(int(t)).strftime("%m/%d/%Y %H:%M:%S")
    
def NaturalToUnix(x):
    return int(time.mktime(datetime.strptime(x, "%m/%d/%Y %H:%M:%S").timetuple()))

#class to extract required data from gate api
class TradingData:
    
    def __init__(self, _coin_name, _interval, _start_date, _end_date):
        self.coin_name = _coin_name 
        self.interval = _interval
        self.start_date = NaturalToUnix(_start_date)
        self.end_date = NaturalToUnix(_end_date)
        self.df = self.fetchData()
    
    def fetchData(self):
        
        configuration = gate_api.Configuration(
            host = "https://api.gateio.ws/api/v4"
        )
        api_client = gate_api.ApiClient(configuration)
        api_instance = gate_api.SpotApi(api_client)
        
        currency_pair = self.coin_name + "_USDT"
        _from = self.start_date
        to = self.end_date
        
        try:
            api_response = api_instance.list_candlesticks(currency_pair, _from=_from, to=to, interval=self.interval)
            
        except GateApiException as ex:
            print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
            exit()
        except ApiException as e:
            print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)
            exit()
            
        l = len(api_response)
        col_names = ['timestamp', 'volume' , 'close', 'high', 'low', 'open', 'candleID']
        df = pd.DataFrame(columns = col_names, index = [i for i in range(1, l+1)])
        i = 1
        for x in api_response:
            tp = [float(a) for a in x]
            tp.append(i)
            df.loc[i] = tp
            i = i+1
            
        return df 

    def plotData(self):
        
        df = self.df
        
        candle = go.Candlestick(
            x = df['timestamp'],
            open = df['open'],
            close = df['close'],
            high = df['high'],
			low = df['low'],
			name = "Candlesticks")

        data = [candle]
        
        layout = go.Layout(title = self.coin_name)
        fig = go.Figure(data = data, layout = layout)

        plot(fig, filename=self.coin_name)
