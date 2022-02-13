import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
def author():
        return 'htang63'

def get_daily_return(df):
    daily_return = (df/df.shift(1)) - 1
    return daily_return

def get_Bollinger_band(df,window = 10):
    SMA = df.rolling(window).mean()
    rolling_std = df.rolling(window).std()
    upper_band = SMA + 2 * rolling_std
    lower_band = SMA - 2 * rolling_std
    percentage_B = (df - lower_band)/(upper_band - lower_band)
    return upper_band,lower_band,percentage_B,SMA

def get_momentum(df,window = 10):
    #a = df.shift(window)
    momentum = df / df.shift(window-1) - 1
    return momentum

def get_volatility(df,window = 10):
    daily_return = get_daily_return(df)
    volatility = daily_return.rolling(window).std()
    return volatility

def get_EMA(df,window = 10,smoothing = 2.0):
    SMA = df.rolling(window).mean()
    EMA = df.copy()
    EMA.iloc[:] = np.NAN
    EMA.iloc[window - 1] = SMA.iloc[window - 1]
    for i in range(window,df.shape[0]):
        EMA.iloc[i] = smoothing/(1 + window) * df.iloc[i] + EMA.iloc[i-1] * (1 - smoothing/(1 + window))
    return EMA

def get_SMA(df,window = 10):
    SMA = df.rolling(window).mean()
    SMA_ratio = df/SMA
    return SMA,SMA_ratio



def indicator_plot():
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    df = get_data(['JPM'],pd.date_range(start_date, end_date))
    df = df.drop("SPY", axis=1)
    df = df/df.iloc[0]

    #1 Bollinger Band Plot
    upper_band,lower_band,percentage_B,SMA = get_Bollinger_band(df, 20)
    plt.plot(df,label="JPM Price" )
    plt.plot(SMA,label="SMA 20 days")
    plt.plot(percentage_B,label="%B value")
    plt.plot(upper_band,label="Bollinger Upper Band")
    plt.plot(lower_band,label="Bollinger Lower Band")
    plt.legend(loc='best')
    plt.title("Bollinger Band")
    plt.ylabel("Normalized Prices")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("figure1")
    plt.close()

    #2 SMA
    SMA20 = df.rolling(20).mean()
    SMA_ratio = df/SMA20
    plt.plot(df,label="JPM Price" )
    plt.plot(SMA_ratio,label="Price / SMA20 ratio" )
    plt.plot(SMA20,label="Simple Moving Average 20 days")
    plt.legend(loc='best')
    plt.title("Simple Moving Average")
    plt.ylabel("Normalized Prices")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("figure2")
    plt.close()

    #3 momentum
    momentum = get_momentum(df,10)
    plt.plot(df,label="JPM Price" )
    plt.plot(momentum,label="momentum")
    plt.legend(loc='best')
    plt.title("Momentum")
    plt.ylabel("Normalized Prices")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("figure3")
    plt.close()

    #4 volatility
    #rolling_std = df.rolling(10).std()
    volatility = get_volatility(df,10)
    plt.plot(df,label="JPM Price" )
    plt.plot(volatility,label="volatility")
    plt.legend(loc='best')
    plt.title("volatility")
    plt.ylabel("Normalized Prices")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("figure4")
    plt.close()

    #5 EMA
    EMA10 = get_EMA(df,10)
    EMA_ratio = df/EMA10
    plt.plot(df,label="JPM Price" )
    plt.plot(EMA10,label="EMA for 10 days")
    plt.plot(EMA_ratio,label="Price / EMA10")
    plt.legend(loc='best')
    plt.title("Exponential Moving Average")
    plt.ylabel("Normalized Prices")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("figure5")
    plt.close()

if __name__ == '__main__':
    indicator_plot()
