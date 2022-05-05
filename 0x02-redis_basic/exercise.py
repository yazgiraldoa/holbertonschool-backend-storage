#!/usr/bin/env python3
"""
Redis basics
"""
from functools import wraps
from typing import Callable, Union, Optional
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a funct is called"""
    @wraps(method)
    def wrapper(*args, **kwds):
        key = method.__qualname__
        self = args[0]
        self._redis.incr(key, 1)
        return method(*args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that saves a list of inputs and outputs"""
    @wraps(method)
    def wrapper(*args, **kwds):
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        self = args[0]

        self._redis.rpush(input_key, str(args[1:]))
        output = method(*args, **kwds)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """Function that displays the history of calls of a particular function"""
    _redis = redis.Redis()
    key = method.__qualname__
    count = int(_redis.get(key))

    input_key = f'{method.__qualname__}:inputs'
    output_key = f'{method.__qualname__}:outputs'

    input_list = _redis.lrange(input_key, 0, count)
    output_list = _redis.lrange(output_key, 0, count)

    print(f'{method.__qualname__} was called {count} times:')
    name = method.__qualname__
    for i, o in zip(input_list, output_list):
        print(f'{name}(*{i.decode("UTF-8")}) -> {o.decode("UTF-8")}')


class Cache:
    """
    Cache class
    """
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, Union[bytes, Union[int, float]]]) -> str:
        """Method to save a key in redis"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[
            Union[str, Union[bytes, Union[int, float]]]
            ]:
        """Method to retrieve a value from redis"""
        v = self._redis.get(key)
        if v and fn:
            return fn(v)
        return v

    def get_str(self, value: Optional[
            Union[str, Union[bytes, Union[int, float]]]
            ]) -> str:
        """Method that returns a str"""
        return str(value)

    def get_int(self, value: Optional[
            Union[str, Union[bytes, Union[int, float]]]
            ]) -> Optional[int]:
        """Method that returns an int"""
        if value:
            return int(value)
        return value
