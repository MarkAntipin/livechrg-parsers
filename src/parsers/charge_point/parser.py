import json
import logging
from settings import Settings
from utils.area import ChargePointArea
from utils.parse_area import parse_area
from utils.setup_logger import setup_logger
from utils.make_request import make_request

settings = Settings()
logger = logging.getLogger(__name__)
setup_logger(logger)
logger.setLevel(level=logging.INFO)


def get_stations_list(
        *,
        area: ChargePointArea,
        stations_num: int = 50
) -> list:
    params = {
        'station_list': {
            'ne_lat': area.ne_lat,
            'ne_lon': area.ne_lon,
            'sw_lat': area.sw_lat,
            'sw_lon': area.sw_lon,
            'page_size': stations_num,  # почему-то иногда результат оказывается в 2 или 3 раза больше заданного
            'sort_by': 'distance',
        }
    }
    url = f'{settings.CHARGEPOINT_STATION_LIST_LINK_BASE}?{json.dumps(params)}'
    response = make_request(url=url)

    if response:
        if 'station_list' in (json_response := response.json()):
            # отдельная проверка на наличие ключа 'error' позволяет получить более полную и точную информацию о
            # возникающих ошибках
            if 'error' in (stations_dict := json_response['station_list']):
                error = stations_dict['error']
                logger.error('Error while receiving station list from %s: %s', url, error)
                return []
            # отдельная проверка на наличие ключа 'stations' нужна, чтобы отлавливать территории
            # без станций (либо из-за проблем на сайте станции могут перестать отображаться на территории)
            if 'stations' in stations_dict:
                return stations_dict['stations']
            logger.info('There are not any stations in this area: %s', url)
            return []
    return []


def get_station_details(station_id: int) -> dict | None:
    response = make_request(url=settings.CHARGEPOINT_STATION_DETAILS_LINK_BASE, params={'deviceId': station_id})
    if response:
        res = response.json()
        if 'error' in res:
            error = res['error']
            logger.error('Error in request for details about station № %s from %s: %s', station_id, response.url, error)
            return
        return res
    logger.error('Info about station № %s has not been received because of error while requesting', station_id)


def get_station_comments(station_id: int) -> dict | None:
    url = f'{settings.CHARGEPOINT_COMMENTS_LINK_BASE}{station_id}'
    response = make_request(url=url)
    if response:
        return response.json()
    logger.error('Comments about station № %s has not been received because of error while requesting', station_id)


def main():
    stations_info: dict = {}
    area = ChargePointArea(ne_lat=45.0, ne_lon=22.0, sw_lat=44.0, sw_lon=23.0)
    stations_list = parse_area(area=area, api_cap=50, get_locations_func=get_stations_list)
    if stations_list:
        for station in stations_list:
            station_id = station['device_id']
            station_details = get_station_details(station_id)
            station_comments = get_station_comments(station_id)
            stations_info[station_id] = {
                'brief_info': station,
                'detailed_info': station_details,
                'comments': station_comments
            }

        with open('stations_info.json', 'w', encoding='utf-8') as file:
            json.dump(stations_info, file)


if __name__ == '__main__':
    main()
