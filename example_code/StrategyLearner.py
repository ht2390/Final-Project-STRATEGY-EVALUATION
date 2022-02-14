import datetime as dt
import numpy as np
import pandas as pd
import util as ut
import indicators as indic
from sklearn.ensemble import RandomForestClassifier

class StrategyLearner(object):
    """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        If verbose = False your code should not generate ANY output.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type verbose: bool  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type impact: float  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param commission: The commission amount charged, defaults to 0.0  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type commission: float  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    """
    # constructor
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Constructor method  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.ndays = 5
        self.learner = RandomForestClassifier(n_estimators=20, bootstrap=True)

    def author(self):
        return ('Your name here')

    def add_evidence(
        self,
        symbol="JPM",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 1, 1),
        sv=10000,
    ):
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Trains your strategy learner over a given time frame.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param symbol: The stock symbol to train on  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type symbol: str  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type sd: datetime  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type ed: datetime  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param sv: The starting value of the portfolio  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type sv: int  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """

        # add your code to do learning here
        #  get the prices dataframe
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        if self.verbose:
            print(prices)

    # get all the indicators values
        upper_band,lower_band,percentage_B,SMA = indic.get_Bollinger_band(prices,10)
        momentum = indic.get_momentum(prices,10)
        SMA,SMA_ratio = indic.get_SMA(prices,10)

        x_train = pd.DataFrame(index=prices.index)
        x_train['SMA_ratio'] = SMA_ratio
        x_train['Bolling_Brand'] = percentage_B
        x_train['momentum'] = momentum
        x_train.fillna(0,inplace=True)
        x_train= x_train[:-self.ndays]

        # n days return
        nday_return = prices.values / prices.shift(self.ndays).values-1
        nday_return = nday_return[~np.isnan(nday_return)]

        # use n days return to generate y_train label : -1 as short 1000 shares, 0 as no shares, + 1 as long 1000 shares
        buy_threshold= 0.02 + self.impact
        sell_threshold= -0.02 - self.impact
        y_train = np.digitize(nday_return,[sell_threshold,buy_threshold]) -1

        # train the random forest models
        x_train= x_train.values
        self.learner.fit(x_train,y_train)

    # this method should use the existing policy and test it against new data
    def testPolicy(
        self,
        symbol="JPM",
        sd=dt.datetime(2009, 1, 1),
        ed=dt.datetime(2010, 1, 1),
        sv=10000,
    ):
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Tests your learner using data outside of the training data  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param symbol: The stock symbol that you trained on on  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type symbol: str  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type sd: datetime  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type ed: datetime  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param sv: The starting value of the portfolio  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type sv: int  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :rtype: pandas.DataFrame  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """


        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[syms]

        # get all the indicators
        upper_band,lower_band,percentage_B,SMA = indic.get_Bollinger_band(prices,10)
        momentum = indic.get_momentum(prices,10)
        SMA,SMA_ratio = indic.get_SMA(prices,10)


        x_test = pd.DataFrame(index=prices.index)
        x_test['SMA_ratio'] = SMA_ratio
        x_test['Bolling_Brand'] = percentage_B
        x_test['momentum'] = momentum
        x_test.fillna(0,inplace=True)

        # call the random forest to do the prediction
        x_test = x_test.values
        y_test = self.learner.predict(x_test)

        df_trade = prices.copy()
        df_trade[symbol] = 0
        holding_shares = 0

        # translate the y_test into trading orders data frame
        for i in range(y_test.shape[0]-1):
            if y_test[i] > 0:
                if holding_shares == 0 :
                    df_trade.iloc[i,0] = 1000
                    holding_shares = 1000
                elif holding_shares == -1000:
                    df_trade.iloc[i,0] = 2000
                    holding_shares = 1000


            elif y_test[i] < 0:
                if holding_shares == 0 :
                    df_trade.iloc[i,0] = -1000
                    holding_shares = -1000
                elif holding_shares == 1000:
                    df_trade.iloc[i,0] = -2000
                    holding_shares = -1000


            else:
                if holding_shares == 1000:
                    df_trade.iloc[i,0] = -1000
                    holding_shares = 0
                elif holding_shares == -1000:
                    df_trade.iloc[i,0] = 1000
                    holding_shares = 0



        return df_trade


if __name__ == "__main__":
    print("One does not simply think up a strategy")
