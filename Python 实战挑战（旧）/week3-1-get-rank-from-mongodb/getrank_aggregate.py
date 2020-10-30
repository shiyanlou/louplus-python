import sys
from pymongo import MongoClient


def get_rank(user_id):
    # 读取数据
    client = MongoClient()
    db = client.shiyanlou

    # 统计指定用户的总分数和总提交时间
    pipeline = [
        # 选取指定用户的记录
        {'$match': {'user_id': user_id}},
        # 按用户 ID 分组统计总分数和总时间，因为只选取了一个用户的记录，所以分组只有一个
        {'$group': {
            '_id': '$user_id',
            'total_score': {'$sum': '$score'},
            'total_time': {'$sum': '$submit_time'}
        }}
    ]

    # 通过 list 转换，读取到所有结果
    results = list(db.contests.aggregate(pipeline))
    # 有可能指定的用户不存在，那么结果集为空
    if len(results) == 0:
        return 0, 0, 0

    data = results[0]

    # 计算指定用户的排名信息
    pipeline = [
        # 分组计算所有用户的总分数和总时间
        {'$group': {
            '_id': '$user_id',
            'total_score': {'$sum': '$score'},
            'total_time': {'$sum': '$submit_time'}
        }},
        # 从上一步的分组结果集里筛选出排在指定用户之前的，也就是总分比指定用户高或者总分相等但总时间较少的
        {'$match': {
            '$or': [
                {'total_score': {'$gt': data['total_score']}},
                {'total_time': {'$lt': data['total_time']},
                 'total_score': data['total_score']
                 }
            ]
        }},
        # 把上一步筛选出来的文档归为一个分组（_id 为 None）并计算总数
        {'$group': {'_id': None, 'count': {'$sum': 1}}}
    ]

    # 通过 list 转换，读取到所有结果
    results = list(db.contests.aggregate(pipeline))

    # 取结果集第一条里的 count 字段值加 1，即为用户排名
    if len(results) > 0:
        rank = results[0]['count'] + 1
    # 如果结果集为空，则表明没有比用户排名高的，该用户排名为 1
    else:
        rank = 1

    return rank, data['total_score'], data['total_time']


if __name__ == '__main__':
    # 判断参数格式
    if len(sys.argv) != 2:
        print("Parameter error.")
        sys.exit(1)

    # 获取用户 ID
    user_id = int(sys.argv[1])

    # 根据用户 ID 获取用户排名，分数和时间
    userdata = get_rank(user_id)
    print(userdata)
