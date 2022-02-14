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

    # finish your code here
    # get all the indicators



   # set up specific rules using if function

 


    return df_trade



def get_normalized_price(df):
    return df/df.iloc[0]

if __name__ == '__main__':
    print("Manual strategy")


