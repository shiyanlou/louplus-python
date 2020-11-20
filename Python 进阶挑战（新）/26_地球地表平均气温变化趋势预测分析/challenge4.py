import pandas as pd
from sklearn.linear_model import LinearRegression as lr

def Temperature():
    temp = pd.read_csv('GlobalSurfaceTemperature.csv')  # 地表气温数据
    temp = temp.iloc[:, 1:].set_index(pd.to_datetime(temp.Year.astype('str')))
    gas = pd.read_csv('GreenhouseGas.csv')              # 温室气体排放数据
    gas = gas.iloc[:, 1:].set_index(pd.to_datetime(gas.Year.astype('str')))
    co2 = pd.read_csv('CO2ppm.csv')                     # CO2 浓度数据
    co2 = co2.iloc[:, 1:].set_index(pd.to_datetime(co2.Year.astype('str')))
    co2.columns = ['CO2PPM']
    df = pd.concat([gas, co2, temp], 1) # 纵向拼接
    # 对前 4 列也就是气体排量和二氧化碳浓度进行纵向填充
    gas_part = df.iloc[:, :4].fillna(method='ffill').fillna(method='bfill')
    data = gas_part['1970': '2010']  # 已知气体数据
    test = gas_part['2011': '2017']  # 预测所依赖的气体数据

    # 根据前几十年的气体数据和温度数据的线性关系
    # 使用未来几年的气体数据预测温度数据
    # 线性关系可以简单理解为 y = kx , 其中 k 是常数
    # 下面的 model 就是我们要获得的 k , 上面的 test 就是 x 
    # model 的 predict 方法根据线性关系 k 和已知气体数据 test 算出温度的值

    model = lr().fit(data, df['1970': '2010'].Median) # 创建气体-温度线性模型
    median = pd.np.round(model.predict(test), 3)      # 根据气体得出温度预测结果
    model = lr().fit(data, df['1970': '2010'].Upper)
    upper = pd.np.round(model.predict(test), 3)
    model = lr().fit(data, df['1970': '2010'].Lower)
    lower = pd.np.round(model.predict(test), 3)
    return list(upper), list(median), list(lower)

if __name__ == '__main__':
    print(Temperature())
