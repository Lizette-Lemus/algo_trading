import yfinance as yf
from algo_trading.strategies import FibonacciEMAStrategy
from algo_trading.strategies import FibonacciStrategy
from algo_trading.backtester import Backtester
from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import mplfinance as mpf
from datetime import timedelta
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay

symbol = 'TSLA'

# Download data for 3 years
print(f"backtesting {symbol}")
levels_start_date = '2020-03-17'
levels_end_date = '2023-03-17'
levels_data = yf.download(symbol, start=levels_start_date, end=levels_end_date)

#Download data for a different time interval
signals_start_date = '2022-06-01'
signals_end_date = '2023-07-01'
signals_data = yf.download(symbol, start=signals_start_date, end=signals_end_date, interval = '5m')

#NOTE: One year of data from alpha demo
#signals_data = pd.read_csv('alphademoclean.csv', parse_dates=['Datetime'], index_col = 'Datetime')

# Instantiate the FibonacciStrategy with separate datasets for levels and signals
retracements = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

short_window = 4
long_window = 9
time_to_close_position = timedelta(minutes=10)
start_time = datetime.time(hour=9, minute=0)
end_time = datetime.time(hour=11, minute=0)

strategy = FibonacciEMAStrategy(levels_data, signals_data, retracements, short_window, long_window, time_to_close_position, start_time, end_time)
# Backtest the strategy using the testing data
backtester = Backtester(strategy)

start_date = pd.Timestamp('2022-06-01')
end_date = pd.Timestamp('2023-06-28')
total_profit = 0
for day in pd.date_range(start_date, end_date, freq=BDay()):
    day_str = day.strftime('%Y-%m-%d')
    profit = backtester.print_signals_for_day(day_str)
    total_profit+=profit
print(f"Total profit: {total_profit}")
