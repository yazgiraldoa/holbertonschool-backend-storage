#!/usr/bin/env python3
"""
Redis basics
"""
from typing import Callable, Union, Optional
import uuid
import redis


class Cache:
    """
    Cache class
    """
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
