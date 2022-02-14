import datetime as dt
import StrategyLearner as sl
import ManualStrategy as man
import marketsimcode as msc
import matplotlib.pyplot as plt
#%matplotlib inline

def author(self):
        return "Your name here"

def get_normalized_price(df):
    return df/df.iloc[0]

def e1_in_sample():
    # manual
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009,12,31)
    df_trade_man = man.testPolicy(symbol="JPM",sd=start_date,ed=end_date,sv=100000)
    # benchmark
    bench_trade = df_trade_man.copy()
    bench_trade[:] = 0
    bench_trade.iloc[0][0] = 1000

    #learner
    learner = sl.StrategyLearner(impact=0.005)
    learner.add_evidence(symbol="JPM", sd=start_date, ed=end_date , sv=100000)
    df_trade_learner = learner.testPolicy(symbol="JPM", sd=start_date, ed=end_date , sv=100000)


    # get the portval. Replace with your own marketsimcode
   # portval_bench = msc.compute_portvals(bench_trade, 100000, 9.95, 0.005,start_date,end_date)
   # portval_man = msc.compute_portvals(df_trade_man, 100000, 9.95, 0.005,start_date,end_date)
   # portval_learner = msc.compute_portvals(df_trade_learner, 100000, 9.95, 0.005,start_date,end_date)

    portval_bench = get_normalized_price(portval_bench)
    portval_man = get_normalized_price(portval_man)
    portval_learner = get_normalized_price(portval_learner)

    # plot
    plt.plot(portval_man,'r',label="Manual Strategy")
    plt.plot(portval_bench,'g',label="Benchmark")
    plt.plot(portval_learner,'black',label="Strategy Learner")

    plt.legend(loc='best')
    plt.title("Manual Strategy VS Benchmark VS Strategy Learner Portfolio Value In Sample Plot")
    plt.ylabel("Normalized Portfolio Value")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("exp1_in_sample")
    plt.close()



def e1_out_sample():
    # manual
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2011,12,31)
    df_trade_man = man.testPolicy(symbol="JPM",sd=start_date,ed=end_date,sv=100000)
    # benchmark
    bench_trade = df_trade_man.copy()
    bench_trade[:] = 0
    bench_trade.iloc[0][0] = 1000

    #learner
    learner = sl.StrategyLearner(impact=0.005)
    learner.add_evidence(symbol="JPM", sd=start_date, ed=end_date , sv=100000)
    df_trade_learner = learner.testPolicy(symbol="JPM", sd=start_date, ed=end_date , sv=100000)


    # get the portval. Replace with your own marketsimcode
   # portval_bench = msc.compute_portvals(bench_trade, 100000, 9.95, 0.005,start_date,end_date)
   # portval_man = msc.compute_portvals(df_trade_man, 100000, 9.95, 0.005,start_date,end_date)
   # portval_learner = msc.compute_portvals(df_trade_learner, 100000, 9.95, 0.005,start_date,end_date)

    portval_bench = get_normalized_price(portval_bench)
    portval_man = get_normalized_price(portval_man)
    portval_learner = get_normalized_price(portval_learner)

    # plot
    plt.plot(portval_man,'r',label="Manual Strategy")
    plt.plot(portval_bench,'g',label="Benchmark")
    plt.plot(portval_learner,'black',label="Strategy Learner")

    plt.legend(loc='best')
    plt.title("Manual Strategy VS Benchmark VS Strategy Learner Portfolio Value Out Sample")
    plt.ylabel("Normalized Portfolio Value")
    plt.xticks(rotation=30)
    plt.xlabel("date")
    plt.savefig("exp1_out_sample")
    plt.close()





if __name__=="__main__":
    e1_in_sample()
    e1_out_sample()
