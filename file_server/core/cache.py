# --------------------------------------------------------------------------
# Caching layer for dynamic keys. This class uses sha256 to generate keys
# and django's core caching system to store data.
# Note: always use get_key method before other methods to get correct keys
# based on KEY_CONVENTIONS.
# (C) 2019 MehrdadEP, Tehran, Iran
# Created at 2020-01-16,  10:06:16
# Author: MehrdadEP
# Email: mehrdadep@outlook.com
# --------------------------------------------------------------------------

from hashlib import sha256

from django.core.cache import cache


class Cache:

    @classmethod
    def set(cls, key, store_value, expiry_time=None):
        """
        Set new (key, value) an cache
        :param key:
        :param store_value:
        :param expiry_time: in seconds
        :return:
        """
        cache_key = cls._get_key(key)
        cache.set(cache_key, store_value, expiry_time)

    @classmethod
    def get(cls, key):
        cache_key = cls._get_key(key)
        return cache.get(cache_key)

    @classmethod
    def delete(cls, key):
        cache_key = cls._get_key(key)
        cache.delete(cache_key)

    @classmethod
    def _get_key(cls, key, ):
        """
        Return sha256 hashed key to store in cache table
        :param key: from KEY_CONVENTIONS
        :return:
        """

        cache_key = sha256(
            str(f"file_server:{key}").encode('utf-8')
        )

        return cache_key.hexdigest()
