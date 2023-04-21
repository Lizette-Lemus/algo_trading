from pydub import AudioSegment
from pydub.playback import play

import yfinance as yf
import time
import datetime
from algo_trading.strategies import FibonacciEMAStrategy
import os
import smtplib
from email.message import EmailMessage

# Download data for 3 years
symbol = 'SPY'
levels_start_date = '2020-03-17'
levels_end_date = '2023-03-17'
levels_data = yf.download(symbol, start=levels_start_date, end=levels_end_date)


retracements = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
short_window = 4 
long_window = 9 
interval = '5m'

from_email = 'llg920420@gmail.com'
to_email = 'llg920420@gmail.com'
password = 'mqwndkvqjgkkejhr'
phone_number = "3037759209"
carrier_gateway = "vtext.com" 


def get_latest_data():
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=1)
    end_date = now + datetime.timedelta(days=1)
    return yf.download(symbol, start=start_date, end=end_date, interval=interval)

def play_alert():
    sound = AudioSegment.from_mp3('/home/lizette/repos/algo_trading/alert.mp3')
    play(sound)

def send_email(subject, body, to_email, from_email, password):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

def send_sms_alert(phone_number, carrier_gateway, message, from_email, password):
    to_email = f"{phone_number}@{carrier_gateway}"
    subject = "Trading Algo Alert"
    send_email(subject, message, to_email, from_email, password)

def send_love():
    love = "Heart over, you make, my life, worth live, and/or, in, the array, I'm only one, that, only on, that of nature."
    return love

while True:
    latest_data = get_latest_data()
    time_to_close_position = datetime.timedelta(minutes=1)
    start_time = datetime.time(hour=9, minute=0)
    end_time = datetime.time(hour=11, minute=0)
    strategy = FibonacciEMAStrategy(levels_data, latest_data, retracements, short_window, long_window, time_to_close_position, start_time, end_time)
    signals = strategy.generate_signals()
    latest_signal = signals.iloc[-1]['positions']
    if latest_signal != 0:
        signal_type = 'Buy' if latest_signal == 1 else 'Sell'
        timestamp = latest_data.index[-1]
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        subject = f'{symbol} - {signal_type} Signal'
        body = f'A {signal_type} signal was generated for {symbol} at {formatted_time} with a close price of {latest_data["Close"][-1]}'
        print(body)
        play_alert()
        send_email(subject, body, to_email, from_email, password)
        send_sms_alert(phone_number, carrier_gateway, body, from_email, password)

    # Wait for 60 seconds before fetching new data
    time.sleep(60)

