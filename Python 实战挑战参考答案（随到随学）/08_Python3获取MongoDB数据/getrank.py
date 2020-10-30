import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    contests = client.shiyanlou.contests
    d = {}
    for i in contests.find():
        u = i['user_id']
        s = i['score']
        t = i['submit_time']
        if d.get(u):
            d[u][0] += s
            d[u][1] += t
        else:
            d[u] = [s, t]
    l = sorted(d.values(), key=lambda x: (-x[0], x[1]))
    for i, j in enumerate(l):
        d[[k for k, v in d.items() if v==j][0]].insert(0, i+1)
    return tuple(d[user_id])

if __name__ == '__main__':
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print('Parameter Error')
        exit()
    print(get_rank(user_id))
