import sys
from pymongo import MongoClient


def get_rank(user_id):
    # 读取数据
    client = MongoClient()
    db = client.shiyanlou

    # 统计指定用户的总分数和总提交时间
    pipeline = [
        {'$match': {'user_id': user_id}},
        {
            '$group': {
                '_id': '$user_id',
                'total_score': {'$sum': '$score'},
                'total_time': {'$sum': '$submit_time'}
            }
        }
    ]

    results = list(db.contests.aggregate(pipeline))
    if len(results) == 0:
        return 0, 0, 0

    data = results[0]

    # 计算指定用户的排名信息
    pipeline = [
        {
            '$group': {
                '_id': '$user_id',
                'total_score': {'$sum': '$score'},
                'total_time': {'$sum': '$submit_time'}
            }
        },
        {
            '$match': {
                '$or': [
                    {'total_score': {'$gt': data['total_score']}},
                    {
                        'total_time': {'$lt': data['total_time']},
                        'total_score': data['total_score']
                    }
                ]
            }
        },
        {'$group': {'_id': None, 'count': {'$sum': 1}}}
    ]

    results = list(db.contests.aggregate(pipeline))

    if len(results) > 0:
        rank = results[0]['count'] + 1
    else:
        rank = 1

    return rank, data['total_score'], data['total_time']


if __name__ == '__main__':
    # 判断参数格式
    if len(sys.argv) != 2:
        print("Parameter error.")
        sys.exit(1)

    # 获取用户 ID
    user_id = sys.argv[1]

    # 根据用户 ID 获取用户排名，分数和时间
    userdata = get_rank(int(user_id))
    print(userdata)
