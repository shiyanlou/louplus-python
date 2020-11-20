import pandas as pd

def co2():
    # 读取 Data 表，第二个参数为 sheet 名字，不写则默认读取第一张 sheet
    data = pd.read_excel('ClimateChange.xlsx')
    # 取 'Series code' 这列中值为 'EN.ATM.CO2E.KT' 的行并设置索引
    data = data[data['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    # 刪掉多余的前五列，只留各年排量数据
    data.drop(data.columns[:5], axis=1, inplace=True)
    # 把数组中值为 '..' 的元素替换成 'NaN'
    data.replace({'..': pd.np.nan}, inplace=True)
    # 对 NaN 空值进行向前和向后填充
    data = data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # 读取 Country 表并设置国家代号为索引，方便合并数据 
    country = pd.read_excel('ClimateChange.xlsx', 'Country'
            ).set_index('Country code')
    # 拼接这俩 Series ：国家总排量和国家收入属于什么群体
    df = pd.concat([data.sum(axis=1), country['Income group']], axis=1)
    # Sum emissions
    sum_emissions = df.groupby('Income group').sum()
    # 设置列名
    sum_emissions.columns = ['Sum emissions']
    # 在 df 中加入一列国家名字
    df[2] = country['Country name']
    # 各收入群体中排放量最高的国家和最高排放量
    highest_emissions = df.sort_values(0, ascending=False).groupby(
            'Income group').head(1).set_index('Income group')
    # 设置列名
    highest_emissions.columns = ['Highest emissions', 'Highest emission country']
    # 各收入群体中排放量最低的国家和最低排放量
    lowest_emissions = df[df[0]>0].sort_values(0).groupby('Income group'
            ).head(1).set_index('Income group')
    # 设置列名
    lowest_emissions.columns = ['Lowest emissions', 'Lowest emission country']
    # 返回全部数据, concat 会自动对 index 排序
    return pd.concat([sum_emissions, highest_emissions, lowest_emissions], 1)

if __name__ == '__main__':
    print(co2())
