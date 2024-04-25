
README

1. Import indicators.py, Marketsimcode.py, ManualStrategy.py, StrategyLearner.py, QLearner.py, experiment1.py, experiment2.py, util.py into a folder 
2. Run the command "PYTHONPATH=..:. python testproject.py" from the same folder
3. Charts will be generated in the same folder and statistics will be displayed in console

***************
indicators.py
***************

PYTHONPATH=..:. python indicators.py

This program implements BBP, Price/SMA, MACD, CCI & Volatility and generates corresponding charts saves in same directory. 
The inputs required to the program are start_date, end_date and symbol which are hard coded in generate_indicators(). Please change them to test additional test cases. This program is a standalone program hence can be tested seperately.


********************************
ManualStrategy.py
********************************

PYTHONPATH=..:. python ManualStrategy.py

This program utilize BBV, CCI, Price/SMA indicators and build a optimal manual strategy and generate trades. This program also calculates porfolio values by importing Marketsimcode.py. This also generates necessary Charts and comparison statistics
This program is a standalone program hence can be tested seperately.

Note: marketsimcode.py, indicators.py is required.

********************************
StrategyLearner.py
********************************

PYTHONPATH=..:. python StrategyLearner.py

This program utilize BBV, CCI, Price/SMA indicators and build a strategic learner using Qlearner and generate trades. This program also calculates porfolio values by importing Marketsimcode.py. This also generates necessary Charts and comparison statistics
This program is a standalone program hence can be tested seperately.

Note: marketsimcode.py, indicators.py,QLearner.py is required.

********************************
experiment1.py
********************************

PYTHONPATH=..:. python experiment1.py

This program compares Manualstrategy vs StrategicLearner for the In-sample data. This program also calculates porfolio values by importing Marketsimcode.py. This also generates necessary Charts and comparison statistics
This program is a standalone program hence can be tested seperately.

Note: ManualStrategy.py, StrategyLearner.py,QLearner.py, marketsimcode.py, indicators.py is required.

********************************
experiment2.py
********************************

PYTHONPATH=..:. python experiment2.py

This program run StrategicLearner for different impact values and analyse the statistics. This program also calculates porfolio values by importing Marketsimcode.py. This also generates necessary Charts and comparison statistics
This program is a standalone program hence can be tested seperately.

Note: StrategyLearner.py, marketsimcode.py, indicators.py is required.

************************
testproject.py
************************


PYTHONPATH=..:. python testproject.py

This program calls ManualStrategy.py, experiment1.py, experiment2.py and generates required charts and statistics

Note: indicators.py, marketsimcode.py, experiment1.py, experiment2.py is required.

