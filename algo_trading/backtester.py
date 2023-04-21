import pandas as pd

class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.signals = self.strategy.generate_signals()
        signal_rows = self.signals[self.signals['positions'] != 0]
    
    def simulate_trades(self, initial_capital=100000.0):
        portfolio = pd.DataFrame(index=self.signals.index)
        portfolio['holdings'] = self.signals['positions'].cumsum() * self.data['Close']
        portfolio['cash'] = initial_capital - (self.signals['positions'] * self.data['Close']).cumsum()
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        portfolio['returns'].fillna(0, inplace=True)
        return portfolio

