import pandas as pd

data = pd.read_csv('alphademo.csv')
data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
data['Datetime'] = pd.to_datetime(data['Datetime'])
data = data.set_index('Datetime')
# Rename the columns
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Create 'Adj Close' column
data['Adj Close'] = data['Close']
data.sort_values(by='Datetime', inplace=True)

print(data)
data.to_csv('alphademoclean.csv')
