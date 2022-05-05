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
        slf = args[0]
        slf._redis.incr(key, 1)
        return method(*args, **kwds)
    return wrapper


class Cache:
    """
    Cache class
    """
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
