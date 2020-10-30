import pandas as pd

def quarter_volume():
    data = pd.read_csv('apple.csv')
    s = pd.Series(list(data.Volume), index=pd.to_datetime(data.Date))
    second_volume = s.resample('q').sum().sort_values()[-2]
    return second_volume
