from time import sleep

from src.repositories.livechrg_api import LiveChargeRepository
from src.repositories.plug_share import PlugShareRepository


class PlugShareService:
    def __init__(self):
        self.plug_share_repo = PlugShareRepository()
        self.live_charge_repo = LiveChargeRepository()

    def save_stations_by_ids(self, station_ids: list[int], steep_time: int = 1) -> None:
        stations = []

        source = 'plug_share'
        for station_id in station_ids:
            station_from_api = self.plug_share_repo.get_station(station_id=station_id)
            if not station_from_api:
                continue

            comments = []
            events = []
            for r in station_from_api['reviews']:
                if r['comment']:
                    comments.append({
                        'text': r['comment'],
                        'created_at': r['created_at'],
                        'source': source,
                        'user_name': r.get('user', {}).get('display_name'),
                        'rating': r['rating'],
                    })
                events.append({
                    'charged_at': r['created_at'],
                    'source': source,
                    'name': r.get('vehicle_make'),
                    'is_problem': bool(r.get('problem'))
                })

            chargers = []
            for s in station_from_api['stations']:
                if network := s.get('network', {}).get('name'):
                    chargers.append({
                        'network': network,
                        'ocpi_ids': s['ocpi_ids'],
                    })

            stations.append({
                'coordinates': {
                    'lat': station_from_api['latitude'],
                    'lon': station_from_api['longitude'],
                },
                'source': {
                    'source': source,
                    'inner_id': station_from_api['id'],
                },
                'chargers': chargers,
                'events': events,
                'comments': comments,
                'geo': station_from_api.get('reverse_geocoded_address_components'),
                'rating': station_from_api.get('score'),
                'address': station_from_api['address'],
                'ocpi_ids': station_from_api['ocpi_ids'],
            })
            sleep(steep_time)
        # save parsed data
        self.live_charge_repo.save_stations(stations=stations)
