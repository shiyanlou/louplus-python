import pymongo, sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    contests = client.shiyanlou.contests
    test = client.shiyanlou.test
    d = {}
    for i in contests.find():
        if d.get(i['user_id']):
            d[i['user_id']][0] += i['score']
            d[i['user_id']][1] += i['submit_time']
        else:
            d[i['user_id']] = [i['score'], i['submit_time']]
    for key, value in d.items():
        if not test.find_one({'id': key}):
            test.insert_one({'id':key, 's': value[0], 't': value[1]})
    l = list(test.find().sort([
        ('s', pymongo.DESCENDING), 
        ('t', pymongo.ASCENDING)
    ]))
    for i, v in enumerate(l):
        if v['id'] == user_id:
            return i+1, v['s'], v['t']


