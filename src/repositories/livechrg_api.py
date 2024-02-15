from settings import settings
from src.utils.make_request import make_request


class LiveChargeRepository:
    def __init__(self):
        self._base_url = settings.LIVE_CHARGE_BASE_URL
        self._auth_token = settings.LIVE_CHARGE_AUTH_TOKEN

    def save_stations(self, stations: list[dict]) -> None:
        make_request(
            url=f'{self._base_url}/api/v1/stations',
            method='POST',
            json={
                'stations': stations
            },
            headers={
                'Authorization': self._auth_token
            }
        )
