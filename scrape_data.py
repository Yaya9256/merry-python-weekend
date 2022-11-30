import requests
import json
import argparse
from datetime import datetime

d = {}
j = {}
FMT = "%Y-%m-%dT%H:%M:%S.000%z"


def get_locations():
    """
    Location list will retrieve dictionary of all Regiojet stops directly from
    the endpoint. Combinations of key - name or alias of the town and
    value - the ID.

    Example:
        'Berlin': 10202072, '柏林': 10202072, ...
    """
    url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
    try:
        r = requests.get(url)
        content = json.loads(r.text)
        for country in content:
            for cities in country['cities']:
                d[cities['name']] = cities['id']
                for allias in cities['aliases']:
                    d[allias] = cities['id']
        return d
    except Exception as e:
        print(f'Error in get_locations: {e}')
        raise ValueError


# location_list = get_locations()
# print(location_list)


# 2022-08-27
def get_journeys(departure_day, from_town, to_town, search_currency):
    journeys = []
    # get id's instead of station coming from CLI
    location_list = get_locations()
    print("get_journeys started")

    url = f'https://brn-ybus-pubapi.sa.cz/restapi/routes' \
          f'/search/simple'

    params = {
        "departureDate": departure_day,
        "fromLocationId": location_list[from_town],
        "fromLocationType": "CITY",
        "locale": "cs",
        "tariffs": "REGULAR",
        "toLocationId": location_list[to_town],
        "toLocationType": "CITY"
    }

    headers = {"X-Currency": search_currency}

    try:
        r = requests.get(url, params=params, headers=headers)
        data = json.loads(r.text)
        for route in data['routes']:
            journeys.append({
                "departure_datetime": datetime.strptime(route["departureTime"],
                                                        FMT),
                "arrivalTime": datetime.strptime(route["arrivalTime"], FMT),
                "source": from_town,
                "destination": to_town,
                "fare": {"amount": route["priceTo"],
                         "currency": search_currency}}
            )

        return journeys

    except Exception as e:
        print(f'Error in get_journeys: {e}')
        raise ValueError


if __name__ == 'main':
    # CLI arguments
    try:
        parser = argparse.ArgumentParser(description='Find RegioJet route')
        parser.add_argument('from_town', type=str,
                            help='Name of town leaving',
                            prefix_chars='-')
        parser.add_argument('to_town', type=str,
                            help='Name of destination',
                            prefix_chars='-')
        parser.add_argument('date', type=str,
                            help='Desired date of departure',
                            prefix_chars='-')

        args = parser.parse_args()

    except Exception:
        print("No CLI args supplied.")

# call get journey to retreive journey details
