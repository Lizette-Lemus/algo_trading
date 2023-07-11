import requests
import time
import pandas as pd

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=5min&month=2023-06&outputsize=full&extended_hours=false&apikey=M8T4CDGX785JM2HU'
r = requests.get(url)
data_dict = r.json()
df = pd.DataFrame(data_dict["Time Series (5min)"])
df = df.T  # Transpose Dataframe for desired results
print("df 2023-06")
print(df)
print(time.sleep(12))
apikey = "M8T4CDGX785JM2HU"
symbol = "TSLA"
interval = "5min"
outputsize = "full"
extended_hours = "false"

# start and end months
start_month = pd.to_datetime('2022-06')
end_month = pd.to_datetime('2023-06')

# list to store dataframes for each month
df_list = []

while start_month <= end_month:
    month = start_month.strftime('%Y-%m')
    print(month)
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize={outputsize}&extended_hours={extended_hours}&apikey={apikey}'
    r = requests.get(url)
    data_dict = r.json()
    df = pd.DataFrame(data_dict["Time Series (5min)"])
    df = df.T  # Transpose Dataframe for desired results
    df_list.append(df)

    # go to next month
    start_month = start_month + pd.DateOffset(months=1)
    time.sleep(12)
# concatenate all dataframes
final_df = pd.concat(df_list)

# print final dataframe
print("final df")
print(final_df)

# save to csv
final_df.to_csv('alphademo.csv')

