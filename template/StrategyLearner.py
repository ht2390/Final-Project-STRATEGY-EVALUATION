import datetime as dt
import numpy as np
import pandas as pd
import util as ut
import indicators as indic
import sklearn

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

    # finish your code here

    
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

    # finish your code here
 

        return df_trade


if __name__ == "__main__":
    print("One does not simply think up a strategy")
