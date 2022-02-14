import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode as msc
import matplotlib.pyplot as plt
import indicators as indic

def author():
        return 'Your name here'

def testPolicy(symbol = "JPM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009,12,31),sv = 100000):
    trade_time = pd.date_range(sd,ed)
    price = get_data([symbol],trade_time).ffill().bfill()
    price = price.drop("SPY", axis=1)
    df_trade = price.copy()
    df_trade[symbol] = 0
    holding_shares = 0


    # get all the indicators
    upper_band,lower_band,percentage_B,SMA = indic.get_Bollinger_band(price,10)
    momentum = indic.get_momentum(price,10)
    SMA,SMA_ratio = indic.get_SMA(price,10)


   # set up specific rules using if function

    for i in range(0,len(price.index)-1):
        if holding_shares == 1000:
            if (SMA_ratio.iloc[i][-1] > 1.1 or percentage_B.iloc[i][-1] > 0.8) and momentum.iloc[i][-1] > 0.1:
                df_trade.iloc[i,0] = -2000
                holding_shares = -1000

            elif (SMA_ratio.iloc[i][-1] > 1.0 or percentage_B.iloc[i][-1] > 0.7) and momentum.iloc[i][-1] > 0.05:
                df_trade.iloc[i,0] = -1000
                holding_shares = 0

            else:
                df_trade.iloc[i,0] = 0
                holding_shares = 1000

        elif holding_shares == -1000:
            if (SMA_ratio.iloc[i][-1] < 0.3 or percentage_B.iloc[i][-1] < 0.2) and momentum.iloc[i][-1] < -0.1:
                df_trade.iloc[i,0] = 2000
                holding_shares = 1000

            elif (SMA_ratio.iloc[i][-1] < 0.4 or percentage_B.iloc[i][-1] < 0.3) and momentum.iloc[i][-1] < -0.05:
                df_trade.iloc[i,0] = 1000
                holding_shares = 0

            else:
                df_trade.iloc[i,0] = 0
                holding_shares = -1000

        elif holding_shares == 0:
            if (SMA_ratio.iloc[i][-1] < 0.5 or percentage_B.iloc[i][-1] < 0.3 ) and momentum.iloc[i][-1] < -0.05:
                df_trade.iloc[i,0] = 1000
                holding_shares = 1000

            elif (SMA_ratio.iloc[i][-1] > 0.8 or percentage_B.iloc[i][-1] > 0.6) and momentum.iloc[i][-1] > 0.05:
                df_trade.iloc[i,0] = -1000
                holding_shares = -1000

            else:
                df_trade.iloc[i,0] = 0
                holding_shares = 0


    return df_trade



def get_normalized_price(df):
    return df/df.iloc[0]

if __name__ == '__main__':
    print("Manual strategy")


