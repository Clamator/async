import time
from functools import wraps


def async_measure_time(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        finish = time.perf_counter() - start
        print(f'it took {finish:0.2f} to execute {func}')
        return result
    return wrap


def measure_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        finish = time.perf_counter() - start
        print(f'it took {finish:0.2f} to execute {func}')
        return result

    return wrap
