import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import get_data, plot_data
import matplotlib.dates as mpdates
from matplotlib.dates import DateFormatter
import indicators as ind
import marketsimcode as ms
from collections import OrderedDict


def build_orders(indicator,sym):
    orders = pd.DataFrame(index=indicator.index,columns=['Shares'])
    total_share = 0
    indicator = indicator.dropna()
    for index, row in indicator.iterrows():
        shares = 0

        #selling point
        row_index = indicator.index.get_loc(index)
        print("row index:"+str(row_index))
        print(indicator.columns.get_loc('bbv'))
        print(indicator.iloc[row_index, indicator.columns.get_loc('bbv')])
        print(indicator.iloc[row_index, indicator.columns.get_loc('CCI')])
        print(indicator.iloc[row_index, indicator.columns.get_loc('PSMA Ratio')])
        curr_bbv = indicator.iloc[row_index, indicator.columns.get_loc('bbv')]
        curr_cci = indicator.iloc[row_index, indicator.columns.get_loc('CCI')]
        curr_psma = indicator.iloc[row_index, indicator.columns.get_loc('PSMA Ratio')]

        if (curr_bbv > 1 and  curr_cci > 100 and curr_psma > 1.05):
            if total_share == -1000:
                continue
            elif total_share == 1000:
                shares = -2000
            elif total_share == 0:
                shares = -1000
            orders.loc[index,'Shares'] = shares
            total_share += shares

        #buying point
        elif (curr_bbv < -1 and  curr_cci < -100) and curr_psma < 0.95:
            if total_share == 1000:
                continue
            elif total_share == -1000:
                shares = 2000
            elif total_share == 0:
                shares = 1000
            orders.loc[index,'Shares'] = shares
            total_share += shares
        else:
            orders.loc[index, 'Shares'] = 0

    #orders.set_index(orders['Date'], inplace=True)
    return orders

def change_trades(df_trades,symbol):
    df_trades = df_trades.dropna()
    orders_df = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    print(orders_df)
    for index, row in df_trades.iterrows():
        new_row = pd.DataFrame({'Date': [index], 'Symbol': [symbol], 'Order': ['BUY'], 'Shares': [row['Shares']]})
        if (row['Shares'] == 0):
            continue
        elif row['Shares'] > 0:
            orders_df = pd.concat([orders_df, new_row], ignore_index=True)
        elif row['Shares'] < 0:
            orders_df = pd.concat([orders_df, new_row], ignore_index=True)

    orders_df = orders_df.dropna(subset=['Date'])
    orders_df.set_index(orders_df['Date'], inplace=True)
    return orders_df

def testPolicy(symbol, sd, ed, sv):

    #Generate necessary indicators
    indicator = ind.generate_indicators([symbol],sd,ed,lookback = 20)

    #Build orders df
    df_trades = build_orders(indicator,symbol)

    #Build df_trades from orders df


    return df_trades

def plot_comparison_insample(insample_portvals, benchmark_portvals, orders):

    #Normalize portfolio values
    insample_portvals = insample_portvals/insample_portvals.iloc[0]
    benchmark_portvals = benchmark_portvals/benchmark_portvals.iloc[0]

    plt.title("Manual Strategy vs Benchmark for insample")
    plt.plot(insample_portvals, label="Manual Strategy",color = 'red')
    plt.plot(benchmark_portvals, label="Benchmark",color = 'green')
    first_buy =0
    first_sell =0
    for index, row in orders.iterrows():
        if orders.loc[index]['Order'] == 'BUY' and first_buy==0:
            first_buy =1
            plt.axvline(x=index, color='blue', ls='dashdot', linewidth='0.6', label='Long')
        elif orders.loc[index]['Order'] == 'SELL' and first_sell==0:
            first_sell=1
            plt.axvline(x=index, color='black', ls='dashdot', linewidth='0.6', label='Short')
        elif orders.loc[index]['Order'] == 'BUY':
            plt.axvline(x=index, color='blue', ls='dashdot', linewidth='0.6')
        elif orders.loc[index]['Order'] == 'SELL':
                plt.axvline(x=index, color='black', ls='dashdot', linewidth='0.6')

    plt.xlabel("Date")
    plt.ylabel("Normed Portfolio values")
    plt.tick_params(rotation=12)
    plt.legend(loc='best')
    plt.grid(color='black', linestyle='dotted')
    plt.savefig("Manual Strategy vs Benchmark insample.png", bbox_inches="tight")
    plt.clf()

def plot_comparison_outsample(insample_portvals, benchmark_portvals, orders):

    #Normalize portfolio values
    insample_portvals = insample_portvals/insample_portvals.iloc[0]
    benchmark_portvals = benchmark_portvals/benchmark_portvals.iloc[0]

    plt.title("Manual Strategy vs Benchmark for outsample")
    plt.plot(insample_portvals, label="Manual Strategy",color = 'red')
    plt.plot(benchmark_portvals, label="Benchmark",color = 'green')
    first_buy =0
    first_sell =0
    for index, row in orders.iterrows():
        if orders.loc[index]['Order'] == 'BUY' and first_buy==0:
            first_buy =1
            plt.axvline(x=index, color='blue', ls='dashdot', linewidth='0.6', label='Long')
        elif orders.loc[index]['Order'] == 'SELL' and first_sell==0:
            first_sell=1
            plt.axvline(x=index, color='black', ls='dashdot', linewidth='0.6', label='Short')
        elif orders.loc[index]['Order'] == 'BUY':
            plt.axvline(x=index, color='blue', ls='dashdot', linewidth='0.6')
        elif orders.loc[index]['Order'] == 'SELL':
                plt.axvline(x=index, color='black', ls='dashdot', linewidth='0.6')

    plt.xlabel("Date")
    plt.ylabel("Normed Portfolio values")
    plt.tick_params(rotation=12)
    plt.legend(loc='best')
    plt.grid(color='black', linestyle='dotted')
    plt.savefig("Manual Strategy vs Benchmark outsample.png", bbox_inches="tight")
    plt.clf()

def generate_statistics(orders,portvals,symbol,sd,ed,sv,commission,impact,sample):

    benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    benchmark_trads = benchmark_trads.append({'Date': portvals.index[0], 'Symbol': symbol, 'Order': 'BUY', 'Shares': 1000}, ignore_index=True)
    benchmark_trads.set_index(benchmark_trads['Date'], inplace=True)
    benchmark_portvals = ms.compute_portvals(benchmark_trads, sd, ed, [symbol], sv, commission=commission, impact=impact)

    ms.get_statistics(portvals, benchmark_portvals)
    if sample =='insample':
        plot_comparison_insample(portvals, benchmark_portvals, orders)
    elif sample == 'outsample':
        plot_comparison_outsample(portvals, benchmark_portvals, orders)

if __name__ == "__main__":
    #symbol = 'ML4T-220'
    #symbol = 'AAPL'
    symbol = 'JPM'
    #symbol = 'SINE_FAST_NOISE'
    #symbol = 'UNH'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    comm = 9.95
    impact = 0.005

    insample_df_trade = testPolicy(symbol, sd=sd, ed=ed, sv=100000)
    insample_orders=change_trades(insample_df_trade,symbol)
    insample_portvals = ms.compute_portvals(insample_orders, sd, ed, [symbol], sv, commission=comm, impact=impact)

    # Build orders dataframe for Benchmark and calculate portfolio
    benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    benchmark_trads = benchmark_trads.append({'Date': insample_portvals.index[0], 'Symbol': symbol, 'Order': 'BUY', 'Shares': 1000}, ignore_index=True)
    benchmark_trads.set_index(benchmark_trads['Date'], inplace=True)
    benchmark_portvals = ms.compute_portvals(benchmark_trads, sd, ed, [symbol], sv, commission=comm, impact=impact)

    generate_statistics(insample_orders,insample_portvals,symbol,sd,ed,sv,comm,impact,"insample")

    # FOR OUTSAMPLE
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)
    sv = 100000

    outsample_df_trade = testPolicy(symbol, sd=sd, ed=ed, sv=100000)
    outsample_orders=change_trades(outsample_df_trade,symbol)
    outsample_portvals = ms.compute_portvals(outsample_orders, sd, ed, [symbol], sv, commission=comm, impact=impact)

    # Calculate portfolio values for Benchmark
    out_benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    out_benchmark_trads = out_benchmark_trads.append({'Date': outsample_portvals.index[0], 'Symbol': symbol, 'Order': 'BUY', 'Shares': 1000}, ignore_index=True)
    out_benchmark_trads.set_index('Date', inplace=True)
    out_benchmark_portvals = ms.compute_portvals(out_benchmark_trads,sd,ed,[symbol],sv,commission=comm,impact=impact)

    #Get Statistics for outsample data
    generate_statistics(outsample_orders,outsample_portvals,symbol,sd,ed,sv,comm,impact,"outsample")

    # Plot and get statistics for porfolio values for Optimal Strategy and Benchmark
    #plot_comparison(outsample_portvals, out_benchmark_portvals,outsample_orders,sample="outsample")

