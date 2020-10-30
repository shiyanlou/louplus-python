# 实现访问频率限制器

## 介绍

API 接口一般都会限制客户端的访问频率，防止客户端发起类似于 DDOS 的攻击。比如在 rmon 项目中，每每个 API 接口都应该限制访问频率。一个简单的频率限制器 可以限制一定时间段内方法的最多执行次数，如果超过访问频率则应该禁止访问。在本次挑战中，你需要基于 Python 语言实现一个简单的频率限制器。

## 挑战

rmon 项目的所有 API 都是基于 HTTP 协议实现的，所以你需要开发一个针对这些 API 接口的频率访问限制器 `RateLimiter`，并在超出频率后禁止访问，返回两个值，其中一个值为为错误信息，内容如下：

```python
{
    "ok": False,
    "message": "limit exceed"
}
```

第二个值为 HTTP 状态码 429。频率访问限制器同时也是一个装饰器，类似于 rmon 项目中的 `rmon.common.decorators.ObjectMustBeExist` 装饰器。你需要在 `~/Code/ratelimit.py` 文件中实现频率限制器 `RateLimiter`, 下面是示例代码：

```python

import collections
import functools
import time

class RateLimiter(object):

    def __init__(self, max_calls, period=1.0)
        self.calls = collections.deque()
        self.period = period
        self.max_calls = max_calls

    def __call__(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 补充代码
            pass
        return wrapped
```


## 要求

- 代码存放的位置 `/home/shiyanlou/Code/ratelimit.py` ； 
- 频率限制器类名应该为 `RateLimiter` ；
- 频率限制的时间为秒，代码中默认限制时间范围为 1 秒；

## 提示

- 可以使用一个双端队列保存每一次的调用时间点。每次访问时，通过判断调用次数(双端队列长度)是否超过最大限制从而确定是否超过频率限制，退出时保存这次调用的时间点，并判断最老和最新调用点之间时长是否超过频率限制器的定义时长从而进行恢复。
- 代码中 `max_calls` 指定了 `period` 时间内最多能调用多少次；

## 知识点

- Python 装饰器;
- 频率计算算法；
