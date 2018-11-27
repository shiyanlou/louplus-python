import pandas as pd


def quarter_volume():
    """ 计算苹果股票季度第二高交易量
    """
    df = pd.read_csv('apple.csv')

    s = df.Volume
    s.index = pd.to_datetime(df.Date)

    second_volume = s.resample('Q').sum().sort_values()[-2]

    return second_volume
