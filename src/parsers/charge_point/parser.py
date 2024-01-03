from pprint import pprint

import httpx

import json



STATION_LIST_LINK_BASE = "https://mc.chargepoint.com/map-prod/v2"
STATION_INFO_LINK_BASE = "https://mc.chargepoint.com/map-prod/v3/station/info"
TIPS_LINK_BASE = "https://account.chargepoint.com/account/v1/driver/tip/"


params_for_station_list_request = {
    "station_list": {
        "screen_width": 500,
        "screen_height": 500,
        "ne_lat": 45.99248923039967,
        "ne_lon": -97.28690881274578,
        "sw_lat": 27.268439039977505,
        "sw_lon": -134.9919869377458,
        "page_size": 50,
        # "page_offset": 50,
        # "sort_by": "distance",
        # "reference_lat": 37.20770443804854,
        # "reference_lon": -116.13944787524578,
    #     "include_map_bound": True,
    #     "filter": {
    #         "price_free": False,
    #         "status_available": False,
    #         "dc_fast_charging": False,
    #         "network_chargepoint": False,
    #         "connector_l1": False,
    #         "connector_l2": False,
    #         "connector_l2_nema_1450": False,
    #         "connector_l2_tesla": False,
    #         "connector_chademo": False,
    #         "connector_combo": False,
    #         "connector_tesla": False,
    #     },
    #     "bound_output": True,
    }

}


def _make_request(url, params):
    # TODO: implement
    # TODO: handle errors
    # TODO: print error
    pass


# TODO: addd f-string here
def get_stations_list() -> dict | None:
    response = httpx.get(
        url=STATION_LIST_LINK_BASE + '?' + json.dumps(params_for_station_list_request)
    )
    if response.is_error:
        # TODO: add print error (status code; error text)
        return
    return response


def get_station_info(station_id: int) -> dict:
    response = httpx.get(
        url=STATION_INFO_LINK_BASE,
        params={'deviceId': station_id}
    )
    if response.is_error:
        # TODO: add print error (status code; error text)
        return
    return response.json()


def get_station_comments(station_id: int) -> dict:
    response = httpx.get(f'{TIPS_LINK_BASE}{station_id}')
    if response.is_error:
        # TODO: add print error (status code; error text)
        return
    return response.json()


def main():
    stations_info: dict = {}

    stations_list = get_stations_list()
    if not stations_list:
        # TODO: handle error
        print('Parser has exited...')
        return

    # TODO: ['station_list']['stations'] move to get_stations_list

    for station in stations_list['station_list']['stations']:
        station_id = station['device_id']

        station_info = get_station_info(station_id=station_id)
        comments = get_station_comments(station_id=station_id)

        stations_info[station_id] = {
            'station_base_info': station,
            'station_full_info': station_info,
            'comments': comments
        }

    # TODO: save in file
    pprint(stations_info)


if __name__ == '__main__':
    r = get_stations_list()
    print(len(r.json()['station_list']['stations']))
    print(r.text)
