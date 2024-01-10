import json
import httpx


# TODO: move on settings
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
        # TODO: remove all extra params
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


# TODO: move to make_request from utils
def _make_request(url: str, **kwargs) -> httpx.Response | None:
    try:
        response = httpx.get(url, **kwargs)
        response.raise_for_status()
        return response
    except httpx.HTTPError as exc:
        print(f'Error while requesting {exc.request.url!r}: {exc}')


# get_stations_list from area (lan, lnt)
def get_stations_list(params: dict | None = None) -> list | None:
    if params is None:
        params = params_for_station_list_request
    url = f'{STATION_LIST_LINK_BASE}?{json.dumps(params)}'
    response = _make_request(url=url)
    if response:
        try:
            # if not 'station_list' in response.json():
            #     return

            res = response.json()['station_list']
            if res.get('stations'):
                return res['stations']
            # TODO: add logger print -> logger
            print(f'There are not any stations in this area: {url}')
            return
        # TODO: json.decoder.JSONDecodeError - нужно ли?
        # TODO: handle KeyError in 'if'
        except (KeyError, json.decoder.JSONDecodeError):
            # TODO: add logger print -> logger
            print(f'Stations_list has not been received from {url}')
            return
    # TODO: add logger print -> logger
    print(f'Stations_list has not been received from {url} because of error while requesting')


# get_all_stations_list from area
def get_all_stations_list(
        max_lat: int | float = 90,
        min_lat: int | float = -90,
        min_lon: int | float = -180,
        max_lon: int | float = 180,
        step: int | float = 10
) -> list:
    all_stations_list = []
    lat = max_lat
    lon = min_lon
    while lat > min_lat:
        while lon < max_lon:
            params = dict(params_for_station_list_request)
            ne_lat = lat
            ne_lon = lon
            sw_lat = max((lat - step), min_lat)
            sw_lon = min((lon + step), max_lon)
            params['ne_lat'] = ne_lat
            params['ne_lon'] = ne_lon
            params['sw_lat'] = sw_lat
            params['sw_lon'] = sw_lon
            stations_list = get_stations_list(params=params)
            if stations_list:
                if len(stations_list) < 50:
                    all_stations_list.extend(stations_list)
                else:
                    all_stations_list.extend(get_all_stations_list(
                        max_lat=ne_lat,
                        min_lat=sw_lat,
                        min_lon=ne_lon,
                        max_lon=sw_lon,
                        step=step / 2
                    ))
            lon = lon + step
        lat -= step
        lon = min_lon
    return all_stations_list


# TODO: see get_stations_list
def get_station_details(station_id: int) -> dict | None:
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
            station_info = get_station_details(station_id)
            station_comments = get_station_comments(station_id)
            stations_info[station_id] = {
                'brief_info': station,
                'detailed_info': station_info,
                'comments': station_comments
            }

        with open('stations_info.json', 'w', encoding='utf-8') as file:
            json.dump(stations_info, file)


if __name__ == '__main__':
    main()
