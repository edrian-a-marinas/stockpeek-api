import logging

from django.core.cache import cache

logger = logging.getLogger("config.cache")


def get_cache(key: str):
    value = cache.get(key)
    if value is not None:
        logger.info(f"CACHE_HIT | key={key}")
        return value
    logger.info(f"CACHE_MISS | key={key}")
    return None


def set_cache(key: str, value, ttl: int):
    cache.set(key, value, ttl)
    logger.info(f"CACHE_SET | key={key} | ttl={ttl}")


def delete_cache(key: str):
    cache.delete(key)
    logger.info(f"CACHE_DELETE | key={key}")


def delete_pattern(pattern: str):
    keys = cache.keys(pattern)
    if keys:
        cache.delete_many(keys)
        logger.info(f"CACHE_DELETE_PATTERN | pattern={pattern} | count={len(keys)}")
