from settings import settings
from src.utils.make_request import make_request


class PlugShareRepository:
    def __init__(self):
        self._base_url = settings.PLUG_SHARE_BASE_URL
        self._auth_token = settings.CHARGE_POINT_AUTH_TOKEN
        self._user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )

    def get_stations(
        self,
        span_lat: float,
        span_lng: float,
        latitude: float,
        longitude: float,
        count: int = 1000,
    ) -> list[dict]:
        response = make_request(
            url=f'{self._base_url}/locations/region',
            params={
                'spanLat': span_lat,
                'spanLng': span_lng,
                'latitude': latitude,
                'longitude': longitude,
                'count': count,
            },
            headers={
                'Authorization': f'Basic {self._auth_token}',
                'User-Agent': self._user_agent,
            }
        )
        if not response:
            return []
        return response.json()

    def get_station(self, station_id: int) -> dict | None:
        response = make_request(
            url=f'{self._base_url}/locations/{station_id}',
            headers={
                'Authorization': f'Basic {self._auth_token}',
                'User-Agent': self._user_agent,
            }
        )
        if not response:
            return None
        return response.json()



