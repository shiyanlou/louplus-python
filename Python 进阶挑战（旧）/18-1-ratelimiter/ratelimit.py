import collections
import time
from functools import wraps

class RateLimiter(object):

    def __init__(self, max_calls, period=1.0):
        self.calls = collections.deque()
        self.period = period
        self.max_calls = max_calls

    def __call__(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if len(self.calls) >= self.max_calls:
                result = ({'ok': False, 'message': 'limit exceed'}, 429)
            else:
                result =  f(*args, **kwargs)
            self.calls.append(time.time())
            while (self.calls[-1] - self.calls[0]) >= self.period:
                self.calls.popleft()
            return result
        return wrapped
