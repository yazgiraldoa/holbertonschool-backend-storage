#!/usr/bin/env python3
"""
Redis basics
"""
from typing import Union
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
