import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
# from Plotter import *
from copy import deepcopy
import math
from heapq import heapify, heappush, heappop

# function to find the trend lines

def FindTrendLines(df, n: int = 20, distance_factor: float = 0.0025):
    
    wind = n//3
    df['minval'] = df[['open', 'close']].min(axis=1)
    df['maxval'] = df[['open', 'close']].max(axis=1)

    df['min'] = df.iloc[argrelextrema(
        df.low.values, np.less_equal, order=wind)[0]]['low']
    df['max'] = df.iloc[argrelextrema(
        df.high.values, np.greater_equal, order=wind)[0]]['high']

    dfMax = df[df['max'].notnull()]
    dfMin = df[df['min'].notnull()]
    
    above_trend = []
        
    for i1, p1 in dfMax.iterrows():
        for i2, p2 in dfMax.iterrows():
            
            if i1 + 1 < i2 and (p1['candleID'] < p2['candleID'] - n):
            
                pty = np.asarray((p1['max'], p2['max']))
                ptx = np.asarray((p1['candleID'], p2['candleID']))
                
                slmx, intermx = np.polyfit(ptx, pty, 1)
                valid_idx = []
                
                for i3 in range(i1+1, i2-1):
                    if not pd.isna(df.iloc[i3,:]['max']):
                        p3 = df.iloc[i3,:]
                        tempx = p3['candleID']
                        tempy = slmx*tempx + intermx
                        
                        if tempy < p3['maxval']: # trend is broken
                            valid_idx = []
                            break        
                        
                        if abs(tempy - p3['max']) < distance_factor*p3['max'] and (tempx < ptx[1] - wind and tempx > ptx[0] + wind):
                            valid_idx.append(i3)
                            # print(i1, i2, i3)
                
                if (p1['max'] <= p2['max']):   #Possible Uptrend
                    if len(valid_idx) > 0:
                        above_trend.append({"i1":i1,"i2":i2,"ptx":ptx, "pty":pty, "slp":slmx, "intercpt":intermx, "trend":"up"})
                        
                else:                           # possible down trend
                    if len(valid_idx) > 0:
                        above_trend.append({"i1":i1,"i2":i2,"ptx":ptx, "pty":pty, "slp":slmx, "intercpt":intermx, "trend":"down"})
                        
    below_trend = []
    
    for i1, p1 in dfMin.iterrows():
        for i2, p2 in dfMin.iterrows():
            
            if i1 + 1 < i2 and (p1['candleID'] < p2['candleID'] - n):
            
                pty = np.asarray((p1['min'], p2['min']))
                ptx = np.asarray((p1['candleID'], p2['candleID']))
                
                slmx, intermx = np.polyfit(ptx, pty, 1)
                valid_idx = []
                
                for i3 in range(i1+1, i2-1):
                    if not pd.isna(df.iloc[i3,:]['min']):
                        p3 = df.iloc[i3,:]
                        tempx = p3['candleID']
                        tempy = slmx*tempx + intermx
                        
                        if tempy > p3['minval']: # trend is broken
                            valid_idx = []
                            break        
                        
                        if abs(tempy - p3['min']) < distance_factor*p3['min'] and (tempx < ptx[1] - wind and tempx > ptx[0] + wind):
                            valid_idx.append(i3)
                            # print(i1, i2, i3)
                
                if (p1['min'] <= p2['min']):   #Possible Uptrend
                    if len(valid_idx) > 0:
                        below_trend.append({"i1":i1,"i2":i2,"ptx":ptx, "pty":pty, "slp":slmx, "intercpt":intermx, "trend":"up"})
                        
                else:                           # possible down trend
                    if len(valid_idx) > 0:
                        below_trend.append({"i1":i1,"i2":i2,"ptx":ptx, "pty":pty, "slp":slmx, "intercpt":intermx, "trend":"down"}) 

    
    remove_above_trend = []
    priceRange = df['max'].max() / df['min'].min()
    
    for t1 in above_trend:
        if t1 in remove_above_trend:
            continue 
        for t2 in above_trend:
            if t2 in remove_above_trend:
                continue
            
            if t1 == t2:
                continue
            
            l1 = math.sqrt((t1["ptx"][0] - t1["ptx"][1])**2) + ((t1["pty"][0] - t1["pty"][1])**2) 
            l2 = math.sqrt((t2["ptx"][0] - t2["ptx"][1])**2) + ((t2["pty"][0] - t2["pty"][1])**2)
            
            slp1 = math.atan(t1['slp'])
            slp2 = math.atan(t2['slp'])
            
            if abs(slp1 - slp2) < 0.013*priceRange and (abs(t1["i1"] - t2["i1"] < wind) or (abs(t1["i2"] - t2["i2"]) < wind)):
                if l1 < l2:
                    remove_above_trend.append(t1)
                else:
                    remove_above_trend.append(t2)
                
    remove_below_trend = []
    
    for t1 in below_trend:
        if t1 in remove_below_trend:
            continue 
        for t2 in below_trend:
            if t2 in remove_below_trend:
                continue
            
            if t1 == t2:
                continue 
            
            l1 = math.sqrt((t1["ptx"][0] - t1["ptx"][1])**2) + ((t1["pty"][0] - t1["pty"][1])**2) 
            l2 = math.sqrt((t2["ptx"][0] - t2["ptx"][1])**2) + ((t2["pty"][0] - t2["pty"][1])**2)
            
            slp1 = math.atan(t1['slp'])
            slp2 = math.atan(t2['slp'])
            
            if abs(slp1 - slp2) < 0.013*priceRange and (abs(t1["i1"] - t2["i1"] < wind) or (abs(t1["i2"] - t2["i2"]) < wind)):
                if l1 < l2:
                    remove_below_trend.append(t1)
                else:
                    remove_below_trend.append(t2)
    
    
    for t in remove_above_trend:
        if t in above_trend:
            above_trend.remove(t)
            
    for t in remove_below_trend:
        if t in below_trend:
            below_trend.remove(t)
        
            
    return above_trend, below_trend    


def FindChannel(df, above_trend, below_trend):
    
    possible_channel = []
    mat = []
    heapify(mat)
    for i1, t1 in enumerate(above_trend):
        curr = []
        for i2, t2 in enumerate(below_trend):
            slp1 = math.atan(t1['slp'])
            slp2 = math.atan(t2['slp'])
            val = abs(slp1 - slp2) ; 
            heappush(mat, [val, i1, i2, slp1, slp2])

    done_above = []
    done_below = []
    total = df.shape[0]
    
    normfactor = (df['max'].max() - df['min'].min())  / total 
        
    for x in mat:
        slp = x[0] 
        i1 = x[1]
        i2 = x[2]
        if i1 in done_above or i2 in done_below:
            continue
        else:
            t1 = above_trend[i1]
            t2 = below_trend[i2]

            l1 = t1["i2"] - t1["i1"]    
            l2 = t2["i2"] - t2["i1"]
            
            ratio = max(l1, l2) / min(l1, l2)
            diff = max(l1, l2) - min(l1, l2)
            overlap = (min(t1["i2"], t2["i2"]) - max(t1["i1"], t2["i1"])) / min(l1, l2)
            
            if slp < 0.05*normfactor and overlap > 0.49 and not (ratio > 2 and diff > 0.2*total):
                
                possible_channel.append([above_trend[i1], below_trend[i2]])
                done_above.append(i1)
                done_below.append(i2)   
    
    opt_channel = []
    
    for x in possible_channel:
        
        t1 = x[0]
        t2 = x[1]
        
        i_start = min(t1["i1"], t2["i1"])
        i_end = max(t1["i2"], t2["i2"])
        
        slmx = t1["slp"]
        intrmx = t1["intercpt"]
        
        # mnabove = i_end
        # mxabove = i_start
        # ctmx = 0 
        # for i in range(i_start, i_end+1):
        #     if not pd.isna(df.iloc[i,:]['max']):
        #         p3 = df.iloc[i,:]
        #         tempx = p3['candleID']
        #         tempy = slmx*tempx + intrmx
                
        #         if tempy > p3['maxval']:
        #             mnabove = min(mnabove, i)
        #             mxabove = max(mxabove, i)
        #         else:
        #             ctmx = ctmx+1
                    
        slmn = t2["slp"]
        intrmn = t2["intercpt"]
        
        # ctmn = 0
        # mnbelow = i_end
        # mxbelow = i_start
        # for i in range(i_start, i_end+1):
        #     if not pd.isna(df.iloc[i,:]['min']):
        #         p3 = df.iloc[i,:]
        #         tempx = p3['candleID']
        #         tempy = slmn*tempx + intrmn
                
        #         if tempy < p3['minval']:
        #             mnbelow = min(mnbelow, i)
        #             mxbelow = max(mxbelow, i)
        #         else:
        #             ctmn = ctmn+1 
            
        # imn = max(mnbelow, mnabove)
        # imx = min(mxbelow, mxabove)    

        imn = i_start
        imx = i_end
        c1 = {"i1":imn, "i2":imx, "slp":slmx, "intercpt": intrmx}
        c2 = {"i1":imn, "i2":imx, "slp":slmn, "intercpt": intrmn}
        
        opt_channel.append([c1, c2])
        
    # pos_above = [t1[0] for t1 in possible_channel]
    # pos_below = [t1[1] for t1 in possible_channel]
    
    return possible_channel, opt_channel