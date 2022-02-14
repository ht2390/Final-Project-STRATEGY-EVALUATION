"""
-----do not edit anything above this line---  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
Student Name: Haoyun Tang (replace with your name)  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
GT User ID: htang63(replace with your User ID)  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
GT ID: 903068557  (replace with your GT ID)  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
"""

import datetime as dt
import os

import numpy as np

import pandas as pd
from util import get_data, plot_data

def author():
        return 'htang63'


def compute_portvals(
    orders_file="./orders/orders.csv",
    start_val=100000,
    commission=9.95,
    impact=0.005,
    start_date = dt.datetime(2008, 1, 1),
    end_date = dt.datetime(2009,12,31)
):
    """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    Computes the portfolio values.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param orders_file: Path of the order file or the file object  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type orders_file: str or file object  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param start_val: The starting value of the portfolio  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type start_val: int  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type commission: float  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type impact: float  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :rtype: pandas.DataFrame  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    """
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # read in the orders file as code from assignment instruction
    if isinstance(orders_file,pd.DataFrame):
        orders_df = orders_file.copy()
    else:
        orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
        orders_df = orders_df.sort_values(by='Date')


  #  start_date = orders_df.index[0]
  #  end_date = orders_df.index[-1]
    Symbol_list = orders_df.columns.values

    # get the form of daily stock prices
    price = get_data(Symbol_list,pd.date_range(start_date, end_date))
    price = price.drop("SPY", axis=1)

    date_trade = price.index
    orders_filter = orders_df.copy()
    orders_filter = orders_filter[(orders_filter.T != 0).any()]
    orders_date = orders_filter.index


    # get the form of status for each trading date
    status_form = get_data(Symbol_list,pd.date_range(start_date, end_date))
    status_form = status_form.drop("SPY", axis=1)
    status_form[Symbol_list] = 0
    status_form["Cash"] = 0
    status_form.iloc[0,-1] = start_val


    Cash = start_val
    portval_result = []

    for m in range(len(date_trade)):

        date = date_trade[m]
        current_price = price.loc[date]
        # copy yesterday old positions status to the new date
        if m >= 1:
            old_date = date_trade[m-1]
            status_form.loc[date] = status_form.loc[old_date]



        if date in orders_date:
        # there is trade happening that date
            for i in range(len(orders_date)):
                if date == orders_date[i]:
                    Symbol_trade = Symbol_list[0]
                    Shares = orders_filter.loc[date][-1]
                    if Shares > 0:
                        Order_type ='BUY'
                    elif Shares < 0:
                        Order_type ='SELL'
                    Order_stock_price = get_data([Symbol_trade], pd.date_range(date, date))[Symbol_trade][0]
                    Trade_cost = Order_stock_price * abs(Shares) * impact + commission
                    if Order_type =='BUY':
                        Cash = Cash - Trade_cost - Order_stock_price * abs(Shares)
                        status_form.loc[date,"Cash"] = Cash
                        status_form.loc[date,Symbol_trade] += abs(Shares)
                    else:
                        Cash = Cash - Trade_cost + Order_stock_price * abs(Shares)
                        status_form.loc[date,"Cash"] = Cash
                        status_form.loc[date,Symbol_trade] -= abs(Shares)

            current_positions = status_form.loc[date]
            current_shares, Cash = current_positions[:-1], current_positions[-1]
            portval_today = (current_price * current_shares).sum() + Cash
            portval_result.append(portval_today)


        # No trade happening that date

        else:
        # copy the posistions and cash from yesterday
            current_positions = status_form.loc[date]
            current_shares, Cash = current_positions[:-1], current_positions[-1]
            portval_today = (current_price * current_shares).sum() + Cash
            portval_result.append(portval_today)

    #start_date = dt.datetime(2008, 1, 1)
   # end_date = dt.datetime(2008, 6, 1)
   # portvals = get_data(["IBM"], pd.date_range(start_date, end_date))
  #  portvals = portvals[["IBM"]]  # remove SPY
    rv = pd.DataFrame(index=date_trade, data=portval_result)

    return rv

