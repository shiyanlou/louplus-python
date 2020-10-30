# -*- coding: utf-8 -*-

import redis
import json

r = redis.StrictRedis(host='127.0.0.1', port=6379)

rlist = [i for i in r.lrange('douban_movie:items', 0, 29)]

scores = []

for i in rlist:
    j = json.loads(str(i, encoding="utf-8"))
    scores.append(float(j['score']))
average = sum(scores) / float(len(scores))

assert average >= 8.0
