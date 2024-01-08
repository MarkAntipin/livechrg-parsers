import json
from pprint import pprint
import httpx

STATION_LIST_LINK_BASE = 'https://mc.chargepoint.com/map-prod/v2'
STATION_INFO_LINK_BASE = 'https://mc.chargepoint.com/map-prod/v3/station/info'
COMMENTS_LINK_BASE = 'https://account.chargepoint.com/account/v1/driver/tip/'

params_for_station_list_request = {
    'station_list': {
        # 'screen_width': 857.5999755859375,
        # 'screen_height': 536,
        'ne_lat': 45.0,
        'ne_lon': 20.0,
        'sw_lat': 44.0,
        'sw_lon': 21.0,
        'page_size': 50,  # почему-то иногда результат оказывается в 2 или 3 раза больше заданного
        'page_offset': '',
        'sort_by': 'distance',
        # 'reference_lat': 30,
        # 'reference_lon': 80,
        'include_map_bound': True,
        'filter': {
            'price_free': False,
            'status_available': False,
            'dc_fast_charging': False,
            'network_chargepoint': False,
            'connector_l1': False,
            'connector_l2': False,
            'connector_l2_nema_1450': False,
            'connector_l2_tesla': False,
            'connector_chademo': False,
            'connector_combo': False,
            'connector_tesla': False,
        },
        'bound_output': True,
    }
}


def _make_request(url: str, **kwargs) -> httpx.Response | None:
    try:
        response = httpx.get(url, **kwargs)
        response.raise_for_status()
        return response
    except httpx.HTTPError as exc:
        print(f'Error while requesting {exc.request.url!r}: {exc}')


def get_stations_list() -> list | None:
    url = f'{STATION_LIST_LINK_BASE}?{json.dumps(params_for_station_list_request)}'
    response = _make_request(url=url)
    if response:
        try:
            res = response.json()['station_list']
            if res.get('stations', None):
                return res['stations']
            print(f'There are not any stations in this area: {url}')
            return
        except (KeyError, json.decoder.JSONDecodeError):
            print(f'Stations_list has not been received from {url}')
            return
    print(f'Stations_list has not been received from {url} because of error while requesting')


def get_station_info(station_id: int) -> dict | None:
    response = _make_request(url=STATION_INFO_LINK_BASE, params={'deviceId': station_id})
    if response:
        try:
            res = response.json()
            if res.get('error', None):
                print(f'Error in request for info about station № {station_id}: {response.url}')
                return
            return res
        except json.decoder.JSONDecodeError:
            print(f'Info about station № {station_id} has not been received from {response.url}')
            return
    print(f'Info about station № {station_id} has not been received because of error while requesting')


def get_station_comments(station_id: int) -> dict | None:
    url = f'{COMMENTS_LINK_BASE}{station_id}'
    response = _make_request(url=url)
    if response:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(f'Comments about station № {station_id} has not been received from {response.url}')
            return
    print(f'Comments about station № {station_id} has not been received because of error while requesting')


def main():
    stations_info: dict = {}
    stations_list = get_stations_list()
    if stations_list:
        for station in stations_list:
            station_id = station['device_id']
            station_info = get_station_info(station_id)
            station_comments = get_station_comments(station_id)
            stations_info[station_id] = {
                'brief_info': station,
                'detailed_info': station_info,
                'comments': station_comments
            }

        with open('stations_info.json', 'w', encoding='utf-8') as file:
            json.dump(stations_info, file)


# stations_list = get_stations_list()
# stations_nums = []
# for station in stations_list:
#     stations_nums.append(station['device_id'])
# pprint(stations_nums)


if __name__ == '__main__':
    main()
