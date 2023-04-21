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


# Download data for 3 years
symbol = 'SPY'
levels_start_date = '2020-03-17'
levels_end_date = '2023-03-17'
levels_data = yf.download(symbol, start=levels_start_date, end=levels_end_date)

#Download data for a different time interval
signals_start_date = '2023-04-20'
signals_end_date = '2023-04-21'
signals_data = yf.download(symbol, start=signals_start_date, end=signals_end_date, interval = '5m')

# Instantiate the FibonacciStrategy with separate datasets for levels and signals
retracements = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

short_window = 4
long_window = 9
time_to_close_position = timedelta(minutes=15)
start_time = datetime.time(hour=9, minute=0)
end_time = datetime.time(hour=11, minute=0)

strategy = FibonacciEMAStrategy(levels_data, signals_data, retracements, short_window, long_window, time_to_close_position, start_time, end_time)

# Backtest the strategy using the testing data
backtester = Backtester(signals_data, strategy)

def plot_signals(data, signals):
    # Remove the timezone information
    data.index = data.index.tz_localize(None)
    signals.index = signals.index.tz_localize(None)
    plt.figure(figsize=(15, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5, color = 'purple')

    buys = signals[signals['positions'] == 1].index
    sells = signals[signals['positions'] == -1].index

    plt.scatter(data.loc[buys].index, data.loc[buys]['Close'], marker='^', color='g', label='Buy', s=100)
    plt.scatter(data.loc[sells].index, data.loc[sells]['Close'], marker='v', color='r', label='Sell', s=100)
    plt.plot(data['short_ema'], label='Short EMA', alpha=0.8, color = 'orange')
    plt.plot(data['long_ema'], label='Long EMA', alpha=0.8, color = 'teal')

    plt.title('Stock Price with Buy and Sell signals')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(loc='best')

    # Adjust x-axis ticks and labels
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)

    plt.show()

def calculate_total_return(portfolio):
    initial_value = portfolio['total'].iloc[0]
    final_value = portfolio['total'].iloc[-1]
    total_return_dollars = final_value - initial_value 
    total_return_percentage = total_return_dollars/ initial_value
    return total_return_dollars, total_return_percentage


plot_signals(signals_data, backtester.signals)
portfolio = backtester.simulate_trades(initial_capital = 1000)

total_return_dollars, total_return_percentage = calculate_total_return(portfolio)
print(f"Total return percentage for the backtested period: {total_return_percentage * 100:.2f}%")
print(f"Total return for the backtested period: {total_return_dollars} dollars")
 
