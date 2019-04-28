import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from sqlalchemy import func, desc, and_, select
from ..db import session, Job, engine


# 获得职位数量排名前十的城市数据
def count_top10(): 
    query = session.query(
            Job.city,  # 城市名儿
            # func 提供 count 方法查询字段的数量，须配合分组实现
            # label 对字段重命名，后面要用
            func.count(Job.city).label('count') 
    # 分组，反向排序，取前十条数据
    ).group_by(Job.city).order_by(desc('count')).limit(10)
    # query 是一个查询对象，需要处理一哈
    return [i._asdict() for i in query]  # 每个 i._asdict() 是一个字典

    # 返回值类似这样：
    # [{'city': '北京', 'count': 59},
    #  {'city': '深圳', 'count': 43},
    #  {'city': '广州', 'count': 38},


# 获得平均薪资排名前十的城市数据
def salary_top10(): 
    query = session.query(
            Job.city,
            func.avg((Job.salary_low+Job.salary_up)/2).label('salary')
    ).filter(and_(Job.salary_low>0, Job.salary_up>0)
    ).group_by(Job.city).order_by(desc('salary')).limit(10)
    query_dict_list = [i._asdict() for i in query]
    for i in query_dict_list:
        i['salary'] = float(format(i['salary'], '.1f'))
    return query_dict_list


# 获得数量排名前十的热门标签数据
def hot_tags():
    # 以下两行语句均可查询数据库并将数据转换为 DataFrame 类型
    # df = pd.read_sql('select tags from jobs', engine)
    df = pd.read_sql(select([Job.tags]), engine)
    # 将标签字符串转换成列表，注意要忽略没有标签的数据，结果为嵌套列表
    tags_list = [i.split() for i in df.tags if i != '""']
    # 将嵌套列表中所有标签放到一个大列表里，生成一个新的 DataFrame 数组
    # [i for l in tags_list for i in l] 同 reduce(lambda a, b: a+b, tags_list)
    tags_df = pd.DataFrame([i for l in tags_list for i in l], columns=['tags'])
    # 对标签数组进行分组求数量，取数量最多的前 10 个
    # 结果数据类型为 Series，索引为标签名，值为标签数量
    return tags_df.groupby('tags').size().sort_values(ascending=False).head(10)


# 根据标签数据画图，将图片放入内存中并返回
def hot_tags_plot(format='png'):
    mpl.rcParams['font.sans-serif'] = ['SimHei']    # 设置中文字体
    mpl.rcParams['axes.unicode_minus'] = False      # 正常显示减号
    mpl.rcParams['figure.figsize'] = 10, 5          # 设置画布宽高，单位英寸
    tags_series = hot_tags()  # 获得数量最多的前十个标签的 Series 数组
    plt.bar(tags_series.index, tags_series.values)  # 画柱状图
    img = BytesIO()  # 开启进入内存空间之门，img 就是内存中的一片地方
    plt.savefig(img, format=format)  # 将图片数据保存到内存中
    return img.getvalue()  # 返回内存中的图片数据

# 工作经验统计
def experience_stat():
    rows = session.query(
        # 拼接字符串
        func.concat(
            Job.experience_low, '-', Job.experience_up, '年'
        ).label('experience'),
        # 分组后，获得字符串的数量
        func.count('experience').label('count')
    ).group_by('experience').order_by(desc('count'))
    return [row._asdict() for row in rows]

# 学历要求统计
def education_stat():
    rows = session.query(
        Job.education,
        func.count(Job.education).label('count')
    ).group_by('education').order_by(desc('count'))
    return [row._asdict() for row in rows]
