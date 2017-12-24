import json
from functools import wraps
 

class RedisCache:

    def __init__(self, redis_client):
        self._redis = redis_client

    def cache(self, timeout=0):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if timeout <= 0:
                    return f(*args, **kwargs)
                key = f.__name__
                raw = self._redis.get(key)
                if not raw:
                    value = f(*args, **kwargs)
                    self._redis.setex(key, timeout, json.dumps(value))
                    return value
                else:
                    return json.loads(raw.decode())
            return wrapped
        return decorator

