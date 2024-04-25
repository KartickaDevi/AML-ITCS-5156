

import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data


def compute_portvals(
        orders,
        start_date,
        end_date,
        symbols,
        start_val=100000,
        commission=0,
        impact=0,

):

    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)
    if prices.shape[1] == 2:
        prices = prices.drop(columns='SPY')
    prices['CASH'] = 1.00

    # prepare and load trades data frame
    trades = pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    trades[prices.columns] = 0.0

    for index, rows in orders.iterrows():
        if rows['Order'] == 'BUY':
            trades.at[index, rows['Symbol']] = trades.at[index, rows['Symbol']] + rows['Shares']
            cost_of_share = prices.at[index, rows['Symbol']] * rows['Shares']
            trades.at[index, 'CASH'] -= (cost_of_share + commission + (cost_of_share * impact))
        elif rows['Order'] == 'SELL':
            trades.at[index, rows['Symbol']] = trades.at[index, rows['Symbol']] - rows['Shares']
            cost_of_share = prices.at[index, rows['Symbol']] * rows['Shares']
            trades.at[index, 'CASH'] += cost_of_share - commission - (cost_of_share * impact)

    # prepare and load holdings data frame
    holdings = pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    holdings[prices.columns] = 0.0

    holdings.at[prices.index[0], 'CASH'] = start_val
    first_run_flag = 0
    for index, rows in trades.iterrows():
        if first_run_flag == 0:
            first_run_flag = 1
            holdings.loc[index] += trades.loc[index]
        else:
            holdings.loc[index] = prev_value + trades.loc[index]
        prev_value = holdings.loc[index]

    # load values data frame and compute daily portfolio value
    values = pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    values[prices.columns] = 0.0
    values = prices * holdings

    portvals = pd.DataFrame(index=prices.index, columns=['VALUE'], dtype=float)
    for index, rows in values.iterrows():
        portvals.at[index, 'VALUE'] = sum(rows)

    return portvals


def get_statistics(portvals,benchmark_portvals):

    # Get Benchmark portfolio statistics
    benchmark_portvals = benchmark_portvals[benchmark_portvals.columns[0]]
    benchmark_daily_returns = np.diff(benchmark_portvals) / benchmark_portvals[0: len(benchmark_portvals) - 1]
    benchmark_cum_ret = (benchmark_portvals[-1] / benchmark_portvals[0]) - 1
    benchmark_avg_daily_ret = round(np.mean(benchmark_daily_returns), 15)
    benchmark_tempdf = pd.DataFrame(benchmark_daily_returns, dtype=float)
    benchmark_std_daily_ret = benchmark_tempdf.std()
    benchmark_sharpe_ratio = round(np.sqrt(252) * benchmark_avg_daily_ret / benchmark_std_daily_ret, 15)

    # Get portfolio
    portvals = portvals[portvals.columns[0]]
    daily_returns = np.diff(portvals) / portvals[0: len(portvals) - 1]
    cum_ret = (portvals[-1] / portvals[0]) - 1
    avg_daily_ret = round(np.mean(daily_returns), 15)
    tempdf = pd.DataFrame(daily_returns, dtype=float)
    std_daily_ret = tempdf.std()
    sharpe_ratio = round(np.sqrt(252) * avg_daily_ret / std_daily_ret, 15)

    # Compare portfolio against Benchmark
    print(f"Sharpe Ratio of Optimal Strategy: {round(sharpe_ratio[0], 12)}")
    print(f"Sharpe Ratio of Benchmark : {round(benchmark_sharpe_ratio[0], 12)}")
    print()
    print(f"Cumulative Return of Optimal Strategy: {round(cum_ret, 12)}")
    print(f"Cumulative Return of Benchmark : {round(benchmark_cum_ret,12)}")
    print()
    print(f"Standard Deviation of Optimal Strategy: {round(std_daily_ret[0], 12)}")
    print(f"Standard Deviation of Benchmark : {round(benchmark_std_daily_ret[0], 12)}")
    print()
    print(f"Average Daily Return of Optimal Strategy: {round(avg_daily_ret, 15)}")
    print(f"Average Daily Return of Benchmark : {round(benchmark_avg_daily_ret, 12)}")
    print()
    print(f"Final Portfolio Value of Optimal Strategy: {portvals[-1]}")
    print(f"Final Portfolio Value of Benchmark: {benchmark_portvals[-1]}")

