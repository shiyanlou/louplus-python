import numpy as np, pandas as pd, matplotlib.pyplot as plt

def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx')
    gdp = data[data['Series code']=='NY.GDP.MKTP.CD'].set_index(
            'Country code').iloc[:, 5:]
    co2 = data[data['Series code']=='EN.ATM.CO2E.KT'].set_index(
            'Country code').iloc[:, 5:]
    gdp.replace({'..': pd.np.nan}, inplace=True)
    co2.replace({'..': pd.np.nan}, inplace=True)
    gdp = gdp.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    co2 = co2.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # gdp 和 co2 里都有整行 NaN 值，求和后变成 0
    df = pd.concat([co2.sum(1), gdp.sum(1)], 1)
    df.columns = ['GDP-SUM', 'CO2-SUM']
    df = df.apply(lambda x:(x-x.min())/(x.max()-x.min()))  # 归一化
    strick_labels, labels_position = [], []  # 刻度标签名称和标签的横坐标
    for i in range(len(df)):
        if df.index[i] in {'USA', 'CHN', 'FRA', 'RUS', 'GBR'}:
            strick_labels.append(df.index[i])
            labels_position.append(i)
    fig = plt.subplot()
    df.plot(title='GDP-CO2', ax=fig, kind='line')
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.xticks(labels_position, strick_labels, rotation='vertical')
    plt.show()
    return fig, np.round(df['CHN':'CHN'].values, 3).tolist()[0]

if __name__ == '__main__':
    print(co2_gdp_plot())
