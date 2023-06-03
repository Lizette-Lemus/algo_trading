import numpy as np
import pandas as pd
from typing import List
from datetime import timedelta
import datetime
import pandas_ta as ta


class BaseStrategy:
    def __init__(self, data):
        self.data = data

    def generate_signals(self):
        raise NotImplementedError("Subclasses should implement this method.")

class FibonacciStrategy(BaseStrategy):
    def __init__(self, levels_data: pd.DataFrame, signals_data: pd.DataFrame, retracements: List[float]):
        super().__init__(signals_data)
        self.levels_data = levels_data
        self.retracements = retracements
        self.fib_levels = self.calculate_fibonacci_levels()

    def calculate_fibonacci_levels(self):
        max_price = self.levels_data['High'].max()
        min_price = self.levels_data['Low'].min()

        # Define your additional retracement levels
        additional_retracements = [0.236, 0.382, 0.5, 0.559, 0.618, 0.786]

        main_levels = [(max_price - min_price) * r + min_price for r in self.retracements]
        main_levels.sort()

        additional_levels = []

        for i in range(len(main_levels) - 1):
            lower_level = main_levels[i]
            upper_level = main_levels[i + 1]
            level_range = upper_level - lower_level

            for r in additional_retracements:
                additional_level = lower_level + level_range * r
                additional_levels.append(additional_level)

        return main_levels + additional_levels

    def get_fibonacci_level(self, price, retracements, fib_levels, level_type='support'):
        if level_type == 'support':
            levels = [level for level in fib_levels if level < price]
        else:
            levels = [level for level in fib_levels if level > price]
        if not levels:
            return np.nan

        return min(levels, key=lambda x: abs(x - price))

    def generate_signals(self):
        signals = pd.DataFrame(index=self.data.index)
        signals['positions'] = 0

        # Generate buy and sell signals based on proximity to Fibonacci levels
        for index, row in self.data.iterrows():
            if any(abs(row['Close'] - level) < (max(self.fib_levels) - min(self.fib_levels)) * 0.01 for level in self.fib_levels):
                signals.loc[index, 'positions'] = 1 if row['Close'] > row['Open'] else -1

        return signals
    
class FibonacciEMAStrategy(FibonacciStrategy):
    def __init__(self, levels_data: pd.DataFrame, signals_data: pd.DataFrame, retracements: List[float], 
                short_window: int, long_window: int, time_to_close_position: timedelta, 
                start_time: datetime.time, end_time: datetime.time):
        super().__init__(levels_data, signals_data, retracements)
        self.short_window = short_window
        self.long_window = long_window
        self.time_to_close_position = time_to_close_position
        self.start_time = start_time
        self.end_time = end_time

    def calculate_adx(self, window=10):
        adx_df = ta.adx(self.data['High'], self.data['Low'], self.data['Close'], length=window)
        self.data['ADX'] = adx_df['ADX_10']

    def generate_signals(self):
        signals = pd.DataFrame(index=self.data.index)
        signals['positions'] = 0
        signals['positions_open'] = False

        # Calculate the short and long EMAs
        self.data['short_ema'] = self.data['Close'].ewm(span=self.short_window, adjust=True).mean()
        self.data['long_ema'] = self.data['Close'].ewm(span=self.long_window, adjust=True).mean()

        #ADX
        self.calculate_adx(window=10)

        for i in range(len(self.data)):
            for current_time, row in self.data.iterrows():
                # Check if the current time is within the allowed trading hours
                if self.start_time <= current_time.time() <= self.end_time:
                    if not signals.loc[current_time, 'positions_open']:
                       buy_signal = ((self.data.loc[current_time, 'short_ema'] >= self.data.loc[current_time, 'long_ema']) &
                              (self.data['short_ema'].shift(1).loc[current_time] < self.data['long_ema'].shift(1).loc[current_time]) &
                              (self.data.loc[current_time, 'ADX'] > 25) &
                              any(abs(self.data.loc[current_time, 'Close'] - level) < (max(self.fib_levels) - min(self.fib_levels)) * 0.1 for level in self.fib_levels))

                        sell_signal = ((self.data.loc[current_time, 'short_ema'] <= self.data.loc[current_time, 'long_ema']) &
                               (self.data['short_ema'].shift(1).loc[current_time] > self.data['long_ema'].shift(1).loc[current_time]) &
                               (self.data.loc[current_time, 'ADX'] > 25) &
                               any(abs(self.data.loc[current_time, 'Close'] - level) < (max(self.fib_levels) - min(self.fib_levels)) * 0.1 for level in self.fib_levels))
                        if buy_signal:
                            signals.loc[current_time, 'positions'] = 1
                            signals.loc[current_time, 'positions_open'] = True
                            close_time = current_time + self.time_to_close_position
                            if close_time in signals.index:
                                signals.loc[close_time, 'positions'] = -1

                        elif sell_signal:
                            signals.loc[current_time, 'positions'] = -1
                            signals.loc[current_time, 'positions_open'] = True
                            close_time = current_time + self.time_to_close_position
                            if close_time in signals.index:
                                signals.loc[close_time, 'positions'] = 1

                    else:
                        if signals.loc[current_time, 'positions'] != 0:
                            signals.loc[current_time, 'positions_open'] = False

            return signals
           
