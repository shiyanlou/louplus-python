from pymongo import MongoClient
from bson.son import SON

def get_rank(user_id):
    haha = MongoClient().shiyanlou

    s = haha.contests.aggregate([
        {'$group': {
            '_id': "$user_id",
            'sum_score': {'$sum': '$score'},
            'sum_time': {'$sum': '$submit_time'}}
        },
        {'$sort': 
            SON([('sum_score', -1), ('sum_time', 1)])
        }
    ])

    rank = 1
    for i, j in enumerate(s):
        if user_id == j['_id']:
            return rank, j['sum_score'], j['sum_time']
        rank += 1

if __name__ == '__main__':
    import sys
    print(get_rank(int(sys.argv[1])))
