import datetime as dt
import numpy as np
import pandas as pd

from util import get_data, plot_data
import ManualStrategy as ms
import indicators as ind
import marketsimcode as msc
import StrategyLearner as stl
import experiment1 as exp1
import experiment2 as exp2


if __name__ == "__main__":

    #Manual Strategy for insample period
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    commission = 9.95
    impact =0.005

    #generate trades for insample period
    df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    orders = ms.change_trades(df_trades,symbol)
    #generate portfolio values
    portval = msc.compute_portvals(orders,sd,ed,[symbol],sv,commission=commission,impact=impact)
    #generate necessary statistics & plots
    ms.generate_statistics(orders,portval,symbol,sd,ed,sv,commission,impact,"insample")

    #Manual Strategy for outsample period
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)
    #generate trades for outsample period
    df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    orders = ms.change_trades(df_trades,symbol)
    #generate portfolio values
    portval = msc.compute_portvals(orders,sd,ed,[symbol],sv,commission=commission,impact=impact)
    #generate necessary statistics & plots

    ms.generate_statistics(orders,portval,symbol,sd,ed,sv,commission,impact,"outsample")

    #Run experiment1
    exp1.perform_exp1()
    exp2.perform_exp2()


