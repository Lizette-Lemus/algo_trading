import pandas as pd

class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy
        self.data = strategy.data
        self.signals = strategy.generate_signals()

    def print_signals_for_day(self, date: str):
        daily_signals = self.signals.loc[date]

        daily_profit = 0.0
        buying_price = None
        if daily_signals['trade_day'].any():  # Check if there was a trade on this day
            first_row = True
            for time, row in daily_signals.iterrows():
                prev_positions = daily_signals['positions'].shift().loc[time]
                prev_positions_open = daily_signals['positions_open'].shift().loc[time]
                if first_row:
                    if row['positions'] > 0:
                        print(f"{time}: Buy signal. Buy price: {row['buy_price']}")
                        buying_price = row['buy_price']
                    elif row['positions'] < 0:
                        print(f"{time}: Sell signal. Sell price: {row['sell_price']}")
                        buying_price = row['sell_price']
                    first_row = False
                elif row['positions'] > 0 and row['positions'] != prev_positions: 
                    print(f"{time}: Buy signal. Buy price: {row['buy_price']}")
                    buying_price = row['buy_price']
                elif row['positions'] < 0 and row['positions'] != prev_positions:
                    print(f"{time}: Sell signal. Sell price: {row['sell_price']}")
                    buying_price = row['sell_price']  # in case of short selling
                elif not first_row and row['positions'] == 0 and not row['positions_open'] and prev_positions_open and prev_positions != 0:
                    close_price = self.data['Close'].loc[time]
                    print(f"{time}: Position closed. Close price: {close_price}")
                    if buying_price is not None:
                        if prev_positions > 0:  # Long position, profit is closing price - buying price
                            daily_profit += close_price - buying_price  
                        else:  # Short position, profit is buying price - closing price
                            daily_profit += buying_price - close_price
                        buying_price = None
                first_row = False

            print(f"Daily profit for {date}: {daily_profit}")

        return daily_profit

