import datetime as dt
import numpy as np
import pandas as pd

from util import get_data, plot_data
import ManualStrategy as ms
import indicators as ind
import marketsimcode as msc
import StrategyLearner as stl

def perform_exp1():
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    commission = 9.95
    impact =0.005

    #Manual Strategy for insample period
    df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    orders = ms.change_trades(df_trades,symbol)
    manual_portval = msc.compute_portvals(orders,sd,ed,[symbol],sv,commission=commission,impact=impact)

    #Strategy learner for insample period
    learner = stl.StrategyLearner(verbose=False, impact=0.0, commission=0.0)  # constructor
    learner.add_evidence(symbol=symbol, sd=sd, ed=ed,sv=sv)  # training phase
    df_trades = learner.testPolicy(symbol, sd, ed,sv)  # testing phase
    orders = learner.change_trades(df_trades,symbol)
    learner_portval = msc.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    #Benchmark for insample period
    manual_portval = manual_portval.dropna()
    benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    new_row = pd.DataFrame([[manual_portval.index[0], symbol, 'BUY', 1000]], columns=['Date', 'Symbol', 'Order', 'Shares'])
    benchmark_trads = pd.concat([benchmark_trads, new_row], ignore_index=True)
    benchmark_trads.set_index(benchmark_trads['Date'], inplace=True)
    benchmark_portvals = msc.compute_portvals(benchmark_trads, sd, ed, [symbol], sv, commission=commission, impact=impact)

    #Get statistics
    print("Statistics for manual strategy vs benchmark for insample")
    msc.get_statistics(manual_portval, benchmark_portvals)
    print("Statistics for strategy learner vs benchmark for insample")
    msc.get_statistics(learner_portval, benchmark_portvals)

    #Plot
    stl.plot_comparison(manual_portval, learner_portval, benchmark_portvals)

if __name__ == "__main__":
    perform_exp1()