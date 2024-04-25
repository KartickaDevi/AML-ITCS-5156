import datetime as dt
import numpy as np
import pandas as pd

from util import get_data, plot_data
import ManualStrategy as ms
import indicators as ind
import marketsimcode as msc
import StrategyLearner as stl
import matplotlib.pyplot as plt


def get_benchmark_statistics(benchmark_portvals):

    # Get Benchmark portfolio statistics
    benchmark_portvals = benchmark_portvals[benchmark_portvals.columns[0]]
    benchmark_daily_returns = np.diff(benchmark_portvals) / benchmark_portvals[0: len(benchmark_portvals) - 1]
    benchmark_cum_ret = (benchmark_portvals[-1] / benchmark_portvals[0]) - 1
    benchmark_avg_daily_ret = round(np.mean(benchmark_daily_returns), 15)
    benchmark_tempdf = pd.DataFrame(benchmark_daily_returns, dtype=float)
    benchmark_std_daily_ret = benchmark_tempdf.std()
    benchmark_sharpe_ratio = round(np.sqrt(252) * benchmark_avg_daily_ret / benchmark_std_daily_ret, 15)

    print(f"Sharpe Ratio of Benchmark : {round(benchmark_sharpe_ratio[0], 12)}")
    print()
    print(f"Cumulative Return of Benchmark : {round(benchmark_cum_ret,12)}")
    print()
    print(f"Standard Deviation of Benchmark : {round(benchmark_std_daily_ret[0], 12)}")
    print()
    print(f"Average Daily Return of Benchmark : {round(benchmark_avg_daily_ret, 12)}")
    print()
    print(f"Final Portfolio Value of Benchmark: {benchmark_portvals[-1]}")

def get_statistics(portvals):

    portvals = portvals[portvals.columns[0]]
    daily_returns = np.diff(portvals) / portvals[0: len(portvals) - 1]
    cum_ret = (portvals[-1] / portvals[0]) - 1
    avg_daily_ret = round(np.mean(daily_returns), 15)
    tempdf = pd.DataFrame(daily_returns, dtype=float)
    std_daily_ret = tempdf.std()
    sharpe_ratio = round(np.sqrt(252) * avg_daily_ret / std_daily_ret, 15)

    print(f"Sharpe Ratio of Strategy Learner: {round(sharpe_ratio[0], 12)}")
    print()
    print(f"Cumulative Return of Strategy Learner: {round(cum_ret, 12)}")
    print()
    print(f"Standard Deviation of Strategy Learner: {round(std_daily_ret[0], 12)}")
    print()
    print(f"Average Daily Return of Strategy Learner: {round(avg_daily_ret, 15)}")
    print()
    print(f"Final Portfolio Value of Strategy Learner: {portvals[-1]}")


def plot_comparison(benchmark_portvals, learner_portval_1, learner_portval_2,learner_portval_3,learner_portval_4,learner_portval_5):
    # Normalize portfolio values

    benchmark_portvals = benchmark_portvals / benchmark_portvals.iloc[0]
    learner_portval_1 = learner_portval_1 / learner_portval_1.iloc[0]
    learner_portval_2 = learner_portval_2 / learner_portval_2.iloc[0]
    learner_portval_3 = learner_portval_3 / learner_portval_3.iloc[0]
    learner_portval_4 = learner_portval_4 / learner_portval_4.iloc[0]
    learner_portval_5 = learner_portval_5 / learner_portval_5.iloc[0]


    plt.plot(benchmark_portvals, label="Benchmark", color='green')
    plt.plot(learner_portval_1, label="Strategy Learner with impact = 0", color='yellow')
    plt.plot(learner_portval_2, label="Strategy Learner with impact = 0.005", color='orange')
    plt.plot(learner_portval_3, label="Strategy Learner with impact = 0.01", color='indigo')
    plt.plot(learner_portval_4, label="Strategy Learner with impact = 0.1", color='blue')
    plt.plot(learner_portval_5, label="Strategy Learner with impact = 0.2", color='violet')

    plt.title("Strategy Learner with different impacts")
    plt.xlabel("Date")
    plt.ylabel("Normed Portfolio values")
    plt.tick_params(rotation=12)
    plt.legend(loc='best')
    plt.grid(color='black', linestyle='dotted')
    plt.savefig("experiment2.png")
    plt.clf()

def perform_exp2():
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    commission = 0
    impact = 0

    #Strategy learner for insample period
    learner = stl.StrategyLearner(verbose=False, impact=0.0, commission=0.0)  # constructor
    learner.add_evidence(symbol=symbol, sd=sd, ed=ed,sv=sv)  # training phase
    df_trades = learner.testPolicy(symbol, sd, ed,sv)  # testing phase
    orders = learner.change_trades(df_trades, symbol)
    learner_portval_1 = msc.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    impact = 0.005
    df_trades = learner.testPolicy(symbol, sd, ed,sv)  # testing phase
    orders = learner.change_trades(df_trades, symbol)
    learner_portval_2 = msc.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    impact = 0.01
    df_trades = learner.testPolicy(symbol, sd, ed, sv)  # testing phase
    orders = learner.change_trades(df_trades, symbol)
    learner_portval_3 = msc.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    impact = 0.1
    df_trades = learner.testPolicy(symbol, sd, ed, sv)  # testing phase
    orders = learner.change_trades(df_trades, symbol)
    learner_portval_4 = msc.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    impact = 0.2
    df_trades = learner.testPolicy(symbol, sd, ed, sv)  # testing phase
    orders = learner.change_trades(df_trades, symbol)
    learner_portval_5 = msc.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    #Benchmark for insample period
    learner_portval_5 = learner_portval_5.dropna()
    benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    new_row = pd.DataFrame([[learner_portval_5.index[0], symbol, 'BUY', 1000]], columns=['Date', 'Symbol', 'Order', 'Shares'])
    benchmark_trads = pd.concat([benchmark_trads, new_row], ignore_index=True)
    benchmark_trads.set_index(benchmark_trads['Date'], inplace=True)
    benchmark_portvals = msc.compute_portvals(benchmark_trads, sd, ed, [symbol], sv, commission=commission, impact=impact)


    #Get statistics
    print("Benchmark Statistics")
    get_benchmark_statistics(benchmark_portvals)

    portvals = [learner_portval_1 ,learner_portval_2 ,learner_portval_3 ,learner_portval_4 ,learner_portval_5]
    impacts = [0,0.005,0.01,.1,.2]
    index =0
    for portval in portvals:
        print("Statistics for Manual Strategy with impact "+str(impacts[index]))
        index +=1
        get_statistics(portval)


    #Plot
    plot_comparison(benchmark_portvals, learner_portval_1, learner_portval_2,learner_portval_3,learner_portval_4,learner_portval_5)

if __name__ == "__main__":
    perform_exp2()