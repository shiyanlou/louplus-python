import pandas as pd, matplotlib.pyplot as plt, matplotlib.ticker as ticker

def climate_plot():
    data = pd.read_excel('ClimateChange.xlsx')
    l = ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 
            'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE']
    data = data[data['Series code'].isin(l)].iloc[:, 6:-1]
    data.replace({'..': pd.np.nan}, inplace=True)
    # 横向填充并纵向求和，结果的数据类型是 Series
    data = data.fillna(method='ffill', axis=1).fillna(method='bfill', 
            axis=1).sum()
    # 改装成 DataFrame
    data = pd.DataFrame(data.values, index=data.index, columns=['Total GHG'])

    gt = pd.read_excel('GlobalTemperature.xlsx')
    gt = gt.iloc[:, [1, 4]].set_index(pd.to_datetime(gt.Date))
    gt.fillna(0, inplace=True)
    # 重采样后取年份区间可以直接使用字符串
    gt_y = gt.resample('a').mean()['1990': '2010']
    gt_q = gt.resample('q').mean()
    df = pd.concat([gt_y.set_index(data.index), data], axis=1)
    df = df.apply(lambda x: (x-x.min())/(x.max()-x.min()))

    fig, axes = plt.subplots(nrows=2, ncols=2)
    ax1 = df.plot(kind='line', figsize=(16, 9), ax=axes[0, 0], xticks=df.index)
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Values')
    ax1.set_xticklabels(df.index, rotation=90)
    # 设置主刻度格式（使用旧的％来格式化刻度的值，％d 表示整数）
    # ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax2 = df.plot(kind='bar', figsize=(16, 9), ax=axes[0, 1])
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Values')
    ax3 = gt_q.plot(kind='area', figsize=(16, 9), ax=axes[1, 0])
    ax3.set_xlabel('Quarters')
    ax3.set_ylabel('Temperature')
    # 所谓核密度分布图，就是各个温度值(x轴)所占总数据比例(y轴)的分布图
    ax4 = gt_q.plot(kind='kde', figsize=(16, 9), ax=axes[1, 1])
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Values')
    plt.show()
    return fig

if __name__ == '__main__':
    print(climate_plot())
