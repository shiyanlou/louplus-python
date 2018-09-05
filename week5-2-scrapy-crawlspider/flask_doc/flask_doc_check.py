# -*- coding: utf-8 -*-

import redis

r = redis.StrictRedis(host='127.0.0.1', port=6379)

llen = r.llen('flask_doc:items')

assert llen >= 70
