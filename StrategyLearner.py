 	   		     		  		  		    	 		 		   		 		  
import datetime as dt
import QLearner as ql
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
import util as ut
import indicators as ind
import marketsimcode as ms
import matplotlib.pyplot as plt
import ManualStrategy as man
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class StrategyLearner(object):

    """  		  	   		     		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		     		  		  		    	 		 		   		 		  
		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    # constructor  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission
        self.ql = ql.QLearner(num_states=1000, num_actions=3, alpha=0.2,gamma=0.9,rar=0.5,radr=0.99,dyna=0,verbose=False)

    def discretize(self, indicators):

        indicators['discrete bbv'] = pd.qcut(indicators['bbv'], 10, labels=range(10))
        indicators['discrete psma'] = pd.qcut(indicators['PSMA Ratio'], 10, labels=range(10))
        indicators['discrete cci'] = pd.qcut(indicators['CCI'], 10, labels=range(10))
        indicators['state'] = indicators['discrete bbv'].astype(str) + indicators['discrete psma'].astype(str)+indicators['discrete cci'].astype(str)
        daily_returns = (indicators['Adj Close'] / indicators['Adj Close'].shift(1)) - 1
        daily_returns = daily_returns[1:]
        indicators = indicators.join(daily_returns.to_frame('daily returns')).dropna()

        return indicators

    def change_trades(self, df_trades,symbol):

        orders = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])        
        for index, row in df_trades.iterrows():
            new_row = pd.DataFrame({'Date': [index], 'Symbol': [symbol], 'Order': ['BUY'], 'Shares': [row['Shares']]})
            if (row['Shares'] == 0):
                continue
            elif row['Shares'] > 0:
                orders = pd.concat([orders, new_row], ignore_index=True)
            elif row['Shares'] < 0:
                orders = pd.concat([orders, new_row], ignore_index=True)
        orders = orders.dropna(subset=['Date'])
        orders.set_index(orders['Date'], inplace=True)

        return orders
  		  	   		     		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		  	   		     		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=10000,
    ):  		  	   		     		  		  		    	 		 		   		 		  

  		  	   		     		  		  		    	 		 		   		 		  
        # add your code to do learning here  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        # example usage of the old backward compatible util function  		  	   		     		  		  		    	 		 		   		 		  
        syms = [symbol]

        #sd = sd - dt. timedelta(28)
        indicators = ind.generate_indicators(syms,sd,ed)
        indicators = indicators.dropna()
        indicators = self.discretize(indicators)

        # Create and train Qlearner
        orders = pd.DataFrame(index=indicators.index, columns=['Date', 'Symbol', 'Order', 'Shares'])
        print("add_evidence")
        print(indicators.iloc[0])
        print("here"+str(int(indicators.iloc[0]['state'])))
        state = indicators.iloc[0]['state']
        action = self.ql.querysetstate(state)

        converged = False
        prev_trade = pd.DataFrame([0])

        while not converged:
            total_shares = 0
            # Build order by iterating each day
            for index, row in indicators.iterrows():
                #shares = 0
                reward = int(total_shares * indicators.loc[index]['daily returns'] * (1- self.impact))
                print("reward= "+str(reward))
                action = self.ql.query(int(indicators.loc[index]['state']), reward)
                if (action == 0):
                    continue
                elif (action == 1):
                    if total_shares == 0:
                        total_shares = total_shares - 1000
                        orders.loc[index]['Shares'] = -1000
                    elif total_shares == 1000:
                        total_shares = total_shares - 2000
                        orders.loc[index]['Shares'] = -2000
                elif (action == 2):
                    if total_shares == 0:
                        total_shares = total_shares + 1000
                        orders.loc[index]['Shares'] = 1000
                    elif total_shares == -1000:
                        total_shares = total_shares + 2000
                        orders.loc[index]['Shares'] = 2000

            if (orders.equals(prev_trade)):
                converged = True
            prev_trade = orders.copy()
  		  	   		     		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		     		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  

        #sd = sd - dt.timedelta(28)
        indicators = ind.generate_indicators([symbol], sd, ed)
        indicators = indicators.dropna()
        indicators = self.discretize(indicators)

        orders = pd.DataFrame(columns=['Shares'], index=indicators.index)
        total_shares = 0

        for index, row in indicators.iterrows():
            action = self.ql.querysetstate(int(indicators.loc[index]['state']))
            orders.loc[index, 'Shares'] = 0
            if (action == 1):
                if total_shares == 0:
                    total_shares = total_shares - 1000
                    orders.loc[index, 'Shares'] = -1000
                elif total_shares == 1000:
                    total_shares = total_shares - 2000
                    orders.loc[index, 'Shares'] = -2000
            elif (action == 2):
                if total_shares == 0:
                    total_shares = total_shares + 1000
                    orders.loc[index, 'Shares'] = 1000
                elif total_shares == -1000:
                    total_shares = total_shares + 2000
                    orders.loc[index, 'Shares'] = 2000
            else:
                orders.loc[index, 'Shares'] = 0

        df_trades = orders
        if self.verbose:
            print(type(df_trades))  # it better be a DataFrame!
        if self.verbose:  		  	   		     		  		  		    	 		 		   		 		  
            print(df_trades)
        if self.verbose:  		  	   		     		  		  		    	 		 		   		 		  
            print(indicators['Adj Close'])

        return df_trades
  		  	   		     		  		  		    	 		 		   		 		  


def plot_comparison(manual_portvals, learner_portval, benchmark_portvals):

    #Normalize portfolio values
    manual_portvals = manual_portvals/manual_portvals.iloc[0]
    benchmark_portvals = benchmark_portvals/benchmark_portvals.iloc[0]
    learner_portval = learner_portval/learner_portval.iloc[0]

    plt.plot(manual_portvals, label="Manual Strategy",color = 'red')
    plt.plot(benchmark_portvals, label="Benchmark",color = 'green')
    plt.plot(learner_portval, label="Strategy Leaner", color='blue')

    plt.title("Benchmark vs Manual Strategy")
    plt.xlabel("Date")
    plt.ylabel("Normed Portfolio values")
    plt.tick_params(rotation=12)
    plt.legend(loc='best')
    plt.grid(color='black', linestyle='dotted')
    plt.savefig("experiment1.png")
    plt.clf()


if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  

    symbol = 'JPM'
    #symbol = 'AAPL'
    #symbol = 'ML4T-220'
    #symbol = 'UNH'
    #symbol = 'SINE_FAST_NOISE'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    commission = 9.95
    impact = 0.005

    learner = StrategyLearner(verbose=False, impact=impact, commission=commission)  # constructor
    learner.add_evidence(symbol=symbol, sd=sd, ed=ed,sv=100000)  # training phase
    df_trades = learner.testPolicy(symbol, sd, ed,sv)  # testing phase for insample
    orders = learner.change_trades(df_trades,symbol)
    insample_portval = ms.compute_portvals(orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    #generate benchmark
    benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    benchmark_trads = benchmark_trads.append({'Date': insample_portval.index[0], 'Symbol': symbol, 'Order': 'BUY', 'Shares': 1000}, ignore_index=True)
    benchmark_trads.set_index(benchmark_trads['Date'], inplace=True)
    benchmark_portvals = ms.compute_portvals(benchmark_trads, sd, ed, [symbol], sv, commission=commission, impact=impact)
    print("Strategic learner insample statistics :")
    ms.get_statistics(insample_portval, benchmark_portvals)

    #Test Outsample data
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)

    out_df_trades = learner.testPolicy(symbol, sd, ed,sv)  # testing phase
    out_orders = learner.change_trades(out_df_trades,symbol)
    outsample_portval = ms.compute_portvals(out_orders, sd, ed, [symbol], sv, commission=commission, impact=impact)

    #benchmark for out of sample
    out_benchmark_trads = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    new_row = pd.DataFrame({'Date': outsample_portval.index[0], 'Symbol': symbol, 'Order': 'BUY', 'Shares': 1000})
    out_benchmark_trads = pd.concat([out_benchmark_trads, new_row], ignore_index=True)
    out_benchmark_trads.set_index(out_benchmark_trads['Date'], inplace=True)
    benchmark_portvals = ms.compute_portvals(out_benchmark_trads,sd,ed,[symbol],sv,commission=commission,impact=impact)
    print()
    print("Strategic learner outsample statistics :")
    ms.get_statistics(outsample_portval, benchmark_portvals)

