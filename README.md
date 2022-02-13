# Final-Project-STRATEGY-EVALUATION
The final project for 2022 Python for Machine Learning &amp; Data Science Masterclass

## Background
Congratulations on completing your study on Machine Learning Masterclass! This is the final assignment to test your handling skills on Python, Numpy, Pandas, and **Scikit-learn**. You will need to implement your previous **marketsimcode** to generate comparing plots for different trading strategies.

## Overview
This final project contains 3 steps of work:
1. **indicator selection** 
 - Technical indicators are very important signals for trading strategy. Choose at least 2 technical indicators from **indicators.py** or add your own technical indicators into it. You need to import **indicators.py** at your next step work.
 - It will be better if you can plot the specifically chosen indicators on your final comparing pictures.(Ie. Bollinger Bands) 

2. **Implement a Manual Strategy** 
 - Using your intuition and the indicators selected above, create a manual rules-based strategy and test it against a stock using your market
 
3. **Implement a Strategy Learner**
 - Created a machine-learning-model strategy learner by using **Scikit-learn** or building up your own codes. Then compare the performance with your manual startegy and benchmark strategy. 
 -  Below are the common choices for you. 
 -  - Classification-based learner: Create a strategy using **Random Forest learner** from **Scikit-learn**
 -  - Reinforcement-based learner: Create a **Q-learning-based** strategy from **Scikit-learn**
 -  - Optimization-based learner: Create a **scan-based** strategy using an optimizer

 - Regardless of your choice above, your learner should work in the following way:
 - - In the training phase (e.g., add_evidence()) your learner will be provided with a stock symbol and a time period. It should use this data to learn a strategy. For instance, a classification-based learner will use this data to make predictions about future price changes.
 - - In the testing phase (e.g., testPolicy()) your learner will be provided a symbol and a date range. All learning should be turned OFF during this phase.
You should use the same indicators as you use in the Manual Strategy in Strategy Learner so we can compare your results. You may optimize your indicators for time (vectorization).
