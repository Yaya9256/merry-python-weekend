import scrape_data
from cache import cache_data
import json
from slugify import slugify
from bson import json_util
import redis
from database import table_model
from read_config import get_redis_info

SEARCH_CURRENCY = "CZK"
DM = '_'
redis_url = get_redis_info()["REDIS_URL"]

"""
TO DO: 
fe
put it up in container 
to some domain 
"""

redis = redis.Redis(host=redis_url, decode_responses=True)


def main(date, src, des):
    """
    Will check redis, if the same key is cached, it will retrieve data
    from Redis, otherwise the data will be cached.
    Data is returned to be displayed as API GET request output.
    Data is stored in Database.
    """
    print('hahaha')

    the_key = f'{slugify(src, separator=DM)}' \
              f':{slugify(des, separator=DM)}' \
              f':{slugify(date)}' \
              f':{slugify(SEARCH_CURRENCY)}'

    # RETRIEVE OR STORE TO REDIS
    if cache_data.retrieve_dictionary(redis, key=the_key) is None:
        journeys_list = scrape_data.get_journeys(date, src, des, SEARCH_CURRENCY)
        data = json.dumps(journeys_list, indent=4, default=json_util.default)
        cache_data.store_dictionary(redis, key=the_key, value=data)

    data = cache_data.retrieve_dictionary(redis, key=the_key)

    for journey in data:
        departure_datetime = journey["departure_datetime"]["$date"]
        arrival_datetime = journey["arrivalTime"]["$date"]
        source = journey["source"]
        destination = journey["destination"]
        amount = journey["fare"]["amount"]
        currency = journey["fare"]["currency"]

        # SAVE TO DB
        table_model.insert_data(source, destination, amount, currency,
                                departure_datetime, arrival_datetime)

    return data
