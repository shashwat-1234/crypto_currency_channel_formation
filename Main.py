from TradingData import *
from Utility import *
from Plotter import *

t = int(input())
n = int(input())

for i in range(1, t+1):
    case = str(input())
    
    x = case.split()
    x[2] += " 00:00:00"
    x[3] += " 23:59:59"        
            
    Data = TradingData(x[0], x[1], x[2], x[3])                                  # Class to extract data from the gate API
    df = Data.df    
    above_trend, below_trend = FindTrendLines(df, n)                            # To first find the trend lines in the data
    
    PlotTrendLines(df, above_trend, below_trend, x[0])
    
    possible_channel, opt_channel = FindChannel(df, above_trend, below_trend)   # Finding of possible channel is done
    
    print("Case " + str(i) + " " + x[0] + ' : ' + str(len(opt_channel)))
    
    if len(opt_channel) > 0:
        for channel in opt_channel:
            c1 = channel[0]
            ix1 = c1["i1"]
            ix2 = c1["i2"]
            t1 = int(df.iloc[ix1-1, :]['timestamp'])
            t2 = int(df.iloc[ix2-1, :]['timestamp'])
            print(str(UnixToNatural(t1)), str(UnixToNatural(t2)))
        
        PlotChannel(df, opt_channel, x[0])
        
