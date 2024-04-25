import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import get_data, plot_data
import matplotlib.dates as mpdates
from matplotlib.dates import DateFormatter


def implement_BBP(prices,sym,start_date,end_date,lookback):
    # Calculate SMA and bollinger bands
    for symbol in sym:
        bbp_indicator = pd.DataFrame(index = prices.index)
        bbp_indicator['Adj Close'] = prices[symbol]
        bbp_indicator['sma'] = prices.rolling(window=lookback).mean()
        bbp_indicator['std_dev'] = prices.rolling(window=lookback,center=False).std()
        bbp_indicator['upper_bb'] = bbp_indicator['sma'] + (2 * bbp_indicator['std_dev'])
        bbp_indicator['lower_bb'] = bbp_indicator['sma'] - (2 * bbp_indicator['std_dev'])
        bbp_indicator['bbp'] = ((prices[symbol] - bbp_indicator['lower_bb']) / (bbp_indicator['upper_bb'] - bbp_indicator['lower_bb']) )
        bbp_indicator['bbv'] = (prices[symbol] - bbp_indicator['sma']) / ( 2* bbp_indicator['std_dev'])
        bbp_indicator['normed bbv'] = bbp_indicator['bbv'] / bbp_indicator['bbv'].iloc[lookback-1]
        bbp_indicator['normed bbp'] = bbp_indicator['bbp'] / bbp_indicator['bbp'].iloc[lookback - 1]
    return bbp_indicator

def implement_price_sma_ratio(prices,sym,start_date,end_date,lookback):

    for symbol in sym:
        psma_indicator = pd.DataFrame(index = prices.index)
        psma_indicator['normed price'] = prices / prices.iloc[0]
        """psma_indicator['normed sma'] = psma_indicator['normed price'].rolling(window=lookback).mean()
        psma_indicator['normed sma'] = psma_indicator['normed sma']/psma_indicator['normed sma'].iloc[lookback-1]
        psma_indicator['PSMA Ratio'] = psma_indicator['normed price']/psma_indicator['normed sma']"""

        psma_indicator['SMA'] = prices[symbol].rolling(lookback).mean()
        price_sma = prices[symbol] / psma_indicator['SMA']
        psma_indicator['PSMA Ratio'] = price_sma / price_sma.iloc[lookback-1]

    return psma_indicator

def implement_macd(prices,sym,lookback):
    macd_indicator = pd.DataFrame(index=prices.index)

    macd_indicator['EMA12'] = prices.ewm(span=12,adjust=False).mean()
    macd_indicator['Normed EMA12'] = macd_indicator['EMA12'] / macd_indicator['EMA12'].iloc[lookback-1]

    macd_indicator['EMA26'] = prices.ewm(span=26,adjust=False).mean()
    macd_indicator['Normed EMA26'] = macd_indicator['EMA26'] / macd_indicator['EMA26'].iloc[lookback-1]

    macd_indicator['MACD'] = macd_indicator['EMA12'] - macd_indicator['EMA26']

    macd_indicator['Signal Line'] = macd_indicator['MACD'].ewm(span=9,adjust=False).mean()


    return macd_indicator

def implement_cci(prices,sym):

    cci_indicator =  pd.DataFrame(index=prices.index)
    cci_indicator['Typical Price'] = (prices['High'] + prices['Low'] + prices['Close']) / 3
    cci_indicator['SMA TP'] = cci_indicator['Typical Price'].rolling(window=20, center = False).mean()
    cci_indicator['STD TP'] = cci_indicator['Typical Price'].rolling(window=20, center = False).std()
    cci_indicator['CCI'] = (cci_indicator['Typical Price'] - cci_indicator['SMA TP']) / (0.015 * cci_indicator['STD TP'])

    return cci_indicator

def implement_volatality(prices,sym):

    volatality_indicator =  pd.DataFrame(index=prices.index)
    volatality_indicator['Daily returns'] = (prices / prices.shift(1) ) -1
    volatality_indicator['Volatility'] = volatality_indicator['Daily returns'].rolling(window=20).std()
    #volatality_indicator['Volatility'] = volatality_indicator['Daily returns'].ewm(span=20,adjust=False).std()

    return volatality_indicator

def generate_indicators(symbols,start_date,end_date, lookback = 20):



    #Read csv
    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)
    prices = prices.drop(columns='SPY')

    #Read csv for High, Low, Close
    dates = pd.date_range(start_date, end_date)
    prices_cci = prices.copy()
    prices_cci = prices_cci.rename(columns={symbols[0]: 'Adj Close'})
    prices_cci = prices_cci.join(get_data(symbols, dates, addSPY=False, colname="High"))
    prices_cci = prices_cci.rename(columns={symbols[0]: 'High'})
    prices_cci = prices_cci.join(get_data(symbols, dates, addSPY=False, colname="Low"))
    prices_cci = prices_cci.rename(columns={symbols[0]: 'Low'})
    prices_cci = prices_cci.join(get_data(symbols, dates, addSPY=False, colname="Close"))
    prices_cci = prices_cci.rename(columns={symbols[0]: 'Close'})

    indicator = pd.DataFrame(index=prices.index)

    #1 Indicator - BBP% and SMA
    bbp_indicator = implement_BBP(prices,symbols,start_date,end_date,lookback)
    indicator = indicator.join(bbp_indicator)


    #2 Indicator - Price/SMA ratio

    psma_indicator = implement_price_sma_ratio(prices,symbols,start_date,end_date,lookback)
    indicator = indicator.join(psma_indicator)


    #3 Indicator - MACD
    macd_indicator = implement_macd(prices,symbols,lookback)
    indicator = indicator.join(macd_indicator)


    #4 CCI
    cci_indicator = implement_cci(prices_cci,symbols)
    indicator = indicator.join(cci_indicator)


    #5 Volatality
    volatality_indicator = implement_volatality(prices,symbols)
    indicator = indicator.join(volatality_indicator)

    print(indicator)
    print(indicator['PSMA Ratio'])
    return indicator


if __name__ == "__main__":
    generate_indicators()