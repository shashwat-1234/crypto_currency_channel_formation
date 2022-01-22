import plotly.graph_objs as go
from matplotlib import pyplot
from plotly.offline import plot
from plotly.io import write_image
import os

def createfolder(direc):
    try:
        os.makedirs(direc)
    except:
        pass


def PlotAddCandleSticks(dfpl):
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])
    
    return fig

def PlotTrendLines(dfpl, above_trend, below_trend, name:str = ""):
    
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])
    i = 0 
    for xy in above_trend:
        x = [xy["i1"], xy["i2"]]
        slp = xy['slp']
        intrcpt = xy['intercpt']
        y = [slp*a + intrcpt for a in x]
        i = i+1
        fig.add_trace(go.Scatter(x = x, y = y, mode='lines', name="above"+str(i)))
        
    i = 0 
    for xy in below_trend:
        x = [xy["i1"], xy["i2"]]
        slp = xy['slp']
        intrcpt = xy['intercpt']
        i = i+1
        y = [slp*a + intrcpt for a in x]
        fig.add_trace(go.Scatter(x = x, y = y, mode='lines', name="below"+str(i)))
    
    folder = 'Plots/' + str(name) + '/Trends/'
    createfolder(folder)
    filename = 'Trends' + '.jpeg'
    write_image(fig, folder + filename, format = 'jpeg')
    
    
def PlotAddTrendLine(fig, xy, name):
    
    x = [xy["i1"], xy["i2"]]
    slp = xy['slp']
    intrcpt = xy['intercpt']
    y = [slp*a + intrcpt for a in x]
    fig.add_trace(go.Scatter(x = x, y = y, mode='lines', name=name))
    
    
def PlotChannel(dfpl, possible_channel, name:str = ""):
    
    i = 0
    folder = 'Plots/' + str(name) + '/Channel'
    createfolder(folder)
    
    # for channel in possible_channel:

    #     fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
    #             open=dfpl['open'],
    #             high=dfpl['high'],
    #             low=dfpl['low'],
    #             close=dfpl['close'])])
        
    #     c1 = channel[0]
    #     c2 = channel[1]
        
    #     PlotAddTrendLine(fig, c1, "above" + str(i))
    #     PlotAddTrendLine(fig, c2, "below" + str(i))     
    #     i = i+1 
        
    #     filename = '/Channel_' + str(i) + '.jpeg'
    #     write_image(fig,folder+filename , format = 'jpeg')
    #     #fig.show()
    