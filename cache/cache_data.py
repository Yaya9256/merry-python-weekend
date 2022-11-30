from redis import Redis
import json
from typing import Optional
import logging
from read_config import get_redis_info

SECS = get_redis_info()["CACHE_TIME"]


def store_dictionary(redis: Redis, key: str, value: str) -> None:
    logging.info("Storing into redis...")
    redis.set(key, value, ex=SECS)


def retrieve_dictionary(redis: Redis, key: str) -> Optional[dict]:
    maybe_data = redis.get(key)
    if maybe_data is None:
        return None
    return json.loads(maybe_data)
