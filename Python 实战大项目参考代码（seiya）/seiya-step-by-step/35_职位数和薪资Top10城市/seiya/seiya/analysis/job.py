from sqlalchemy import func, desc, and_
from ..db import session, Job


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
