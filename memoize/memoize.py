import functools
import datetime


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


# можно описать это через класс с вызово __call__(self, *args, **kwargs)
class mem(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in self.cache:
            self.cache[key] = self.func(*args, **kwargs)
        return self.cache[key]


@dec
def func 
==> func = dec(func)

@dec(param)
def func
==> func = dec(param)(func)


def mem(max_size=None, max_time=None):
    def memoize(obj):
        # здесь добавить учет max_size:
        # if max_size not none add key to cache_order_list and
        # kick cache from list where length of queue > max_size:
        # add timestamp to obj.cache objects and check timestamp of prev. cache value:
        cache_order = obj.cache_order = []
        cache = obj.cache = {}

        @functools.wraps(obj)
        def memoizer(*args, **kwargs):
            key = str(args) + str(kwargs)
            if max_size:
                if len(cache_order) > max_size:
                    cache[cache_order[0]].discard() # pop
                    # 
            if max_time:

            if key not in cache:
                # cache[key] = {'result': None, 'timestamp': None}
                cache[key] = obj(*args, **kwargs)
            return cache[key]
        return memoizer
    return memoize
