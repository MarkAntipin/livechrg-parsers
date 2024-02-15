from time import sleep

import pandas as pd

from src.repositories.charge_point import ChargePointRepository
from src.repositories.livechrg_api import LiveChargeRepository


class ChargePointService:
    def __init__(self):
        self.charge_pont_repo = ChargePointRepository()
        self.live_charge_repo = LiveChargeRepository()

    def get_comments(self, station_id: int) -> list[dict]:
        comments = []
        offset_code = 1
        while True:
            comments_from_api, allow_paginate = self.charge_pont_repo.get_comments(
                station_id=station_id, offset_code=offset_code
            )
            if not comments_from_api:
                break

            comments.extend(comments_from_api)

            if not allow_paginate:
                break
            offset_code += 1
        return comments

    def save_stations_by_ids(self, station_ids: list[int], steep_time: int = 1) -> None:
        stations = []

        source = 'charge_point'
        for station_id in station_ids:
            station_from_pai = self.charge_pont_repo.get_station(station_id=station_id)
            if not station_from_pai:
                continue

            comments_from_api = self.get_comments(station_id=station_id)

            events = []
            for event in station_from_pai.get('lastChargedVehicles', []):
                events.append({
                    'charged_at': pd.to_datetime(event['chargedTime'], utc=True, unit='ms').isoformat(),
                    'name': event['name'],
                    'source': source,
                    'is_problem': False,
                })

            comments = []
            for comment in comments_from_api:
                comments.append({
                    'text': comment['text'],
                    'created_at': pd.to_datetime(comment['lastSubmittedTime'], utc=True, unit='ms').isoformat(),
                    'user_name': comment['evatarName'],
                    'source': source,
                })

            stations.append({
                'coordinates': {
                    'lat': station_from_pai['latitude'],
                    'lon': station_from_pai['longitude'],
                },
                'source': {
                    'source': source,
                    'inner_id': station_from_pai['deviceId'],
                },
                'events': events,
                'comments': comments,
                'geo': station_from_pai['address'],
            })
            sleep(steep_time)

        # save parsed data
        self.live_charge_repo.save_stations(stations=stations)
