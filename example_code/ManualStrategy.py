import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode as msc
import matplotlib.pyplot as plt
import indicators as indic

def author():
        return 'Your Name here'

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


def portval_in_sample_plot():

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009,12,31)
    df_trade= testPolicy(symbol="JPM",sd=start_date,ed=end_date,sv=100000)
    buy_points = df_trade.loc[df_trade['JPM'] > 0]
    sell_points = df_trade.loc[df_trade['JPM'] < 0]
    # get the bench trade form
    bench_trade = df_trade.copy()
    bench_trade[:] = 0
    bench_trade.iloc[0][0] = 1000

    # get the bench portval and optimized portval
    portval_opt = msc.compute_portvals(df_trade, 100000, 9.95, 0.005,start_date,end_date)
    portval_bench = msc.compute_portvals(bench_trade, 100000, 9.95, 0.005,start_date,end_date)
    portval_opt = get_normalized_price(portval_opt)
    portval_bench = get_normalized_price(portval_bench)

    plt.plot(portval_opt,'r',label="Manual Strategy")
    plt.plot(portval_bench,'g',label="Benchmark")
    for date in buy_points.index:
        plt.axvline( x = date, c = 'blue')
    for date in sell_points.index:
        plt.axvline( x = date, c = 'black')
    plt.legend(loc='best')
    plt.title("Manual Strategy VS Benchmark Portfolio Value ")
    plt.ylabel("Normalized Portfolio Value")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("Manual_Strategy_figure_VS_bench_in_sample")
    plt.close()


    # parameter calculator
    daily_ret_opt = (portval_opt/portval_opt.shift(1)) - 1
    daily_ret_bench = (portval_bench/portval_bench.shift(1)) - 1
    std_opt = daily_ret_opt.std()
    std_bench = daily_ret_bench.std()

    mean_opt = daily_ret_opt.mean()
    mean_bench = daily_ret_bench.mean()
    cum_ret_opt = portval_opt.iloc[-1]/portval_opt.iloc[0] - 1
    cum_ret_bench = portval_bench.iloc[-1]/portval_bench.iloc[0] - 1

    print("Benchmark: in sample")
    print(f"Standard Deviation of daily return:{std_bench.values}")
    print(f"Mean Value of daily return:{mean_bench.values}")
    print(f"Cumulative return:{cum_ret_bench.values}")
    print("\n")

    print("Manual Strategy: in sample")
    print(f"Standard Deviation of daily return:{std_opt.values}")
    print(f"Mean Value of daily return:{mean_opt.values}")
    print(f"Cumulative return:{cum_ret_opt.values}")
    print("\n")
def portval_out_sample_plot():
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2011,12,31)
    df_trade = testPolicy(symbol="JPM",sd=start_date,ed=end_date,sv=100000)
    buy_points = df_trade.loc[df_trade['JPM'] > 0]
    sell_points = df_trade.loc[df_trade['JPM'] < 0]

        # get the bench trade form
    bench_trade = df_trade.copy()
    bench_trade[:] = 0
    bench_trade.iloc[0][0] = 1000


    # get the bench portval and optimized portval
    portval_opt = msc.compute_portvals(df_trade, 100000, 9.95, 0.005,start_date,end_date)
    portval_bench = msc.compute_portvals(bench_trade, 100000, 9.95, 0.005,start_date,end_date)
    portval_opt = get_normalized_price(portval_opt)
    portval_bench = get_normalized_price(portval_bench)

    plt.plot(portval_opt,'r',label="Manual Strategy")
    plt.plot(portval_bench,'g',label="Benchmark")
    for date in buy_points.index:
        plt.axvline( x = date, c = 'blue')
    for date in sell_points.index:
        plt.axvline( x = date, c = 'black')
    plt.legend(loc='best')
    plt.title("Manual Strategy VS Benchmark Portfolio Value ")
    plt.ylabel("Normalized Portfolio Value")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("Manual_Strategy_figure_VS_bench_out_sample")
    plt.close()

    # parameter calculator
    daily_ret_opt = (portval_opt/portval_opt.shift(1)) - 1
    daily_ret_bench = (portval_bench/portval_bench.shift(1)) - 1
    std_opt = daily_ret_opt.std()
    std_bench = daily_ret_bench.std()

    mean_opt = daily_ret_opt.mean()
    mean_bench = daily_ret_bench.mean()
    cum_ret_opt = portval_opt.iloc[-1]/portval_opt.iloc[0] - 1
    cum_ret_bench = portval_bench.iloc[-1]/portval_bench.iloc[0] - 1

    print("Benchmark: out of sample")
    print(f"Standard Deviation of daily return:{std_bench.values}")
    print(f"Mean Value of daily return:{mean_bench.values}")
    print(f"Cumulative return:{cum_ret_bench.values}")
    print("\n")

    print("Manual Strategy: out of sample")
    print(f"Standard Deviation of daily return:{std_opt.values}")
    print(f"Mean Value of daily return:{mean_opt.values}")
    print(f"Cumulative return:{cum_ret_opt.values}")
    print("\n")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    portval_in_sample_plot()
    portval_out_sample_plot()


