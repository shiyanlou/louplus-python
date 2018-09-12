import pandas as pd


def quarter_volume():
    """ 计算苹果股票季度第二高交易量
    """
    data = pd.read_csv('apple.csv', header=0)

    s = data.Volume
    s.index = pd.to_datetime(data.Date)

    second_volumn = s.resample('Q').sum().sort_values()[-2]

    return second_volumn
