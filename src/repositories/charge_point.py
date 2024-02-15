from settings import settings
from src.utils.make_request import make_request


class ChargePointRepository:
    def __init__(self):
        self._base_url = settings.CHARGE_POINT_BASE_URL
        self._comments_url = settings.CHARGE_POINT_BASE_URL

    def get_stations(
        self,
        ne_lat: float,
        ne_lon: float,
        sw_lat: float,
        sw_lon: float,
        count: int = 50,
    ) -> list[dict]:
        response = make_request(
            url=f'{self._base_url}/map-prod/v2',
            method='POST',
            json={
                'station_list': {
                    'ne_lat': ne_lat,
                    'ne_lon': ne_lon,
                    'sw_lat': sw_lat,
                    'sw_lon': sw_lon,
                    'page_size': count,
                }
            },
        )
        if not response:
            return []
        return response.json()['station_list'].get('stations', [])

    def get_station(self, station_id: int) -> dict | None:
        response = make_request(
            url=f'{self._base_url}/map-prod/v3/station/info',
            params={
                'deviceId': station_id
            }
        )
        if not response:
            return None
        return response.json()

    def get_comments(
        self,
        station_id: int,
        page_size: int = 10,
        offset_code: int = 1
    ) -> tuple[list[dict] | None, bool]:
        response = make_request(
            url=f'{self._comments_url}/account/v1/driver/tip/{station_id}',
            params={
                'offsetCode': offset_code,
                'pageSize': page_size
            }
        )
        if not response:
            return None, False

        if not response.json().get('tips'):
            return None, False

        comments_data = response.json()
        return comments_data['tips'], comments_data.get('offsetCode') != 'last_page'
