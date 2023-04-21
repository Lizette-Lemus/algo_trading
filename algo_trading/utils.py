import pandas as pd

def load_data_from_csv(file_path, index_col='Date', parse_dates=True):
    data = pd.read_csv(file_path, index_col=index_col, parse_dates=parse_dates)
    return data


