from src.services.charge_point import ChargePointService
from src.services.plug_share import PlugShareService


def update_stations_by_ids(station_ids: list[int]) -> None:
    charge_point_service = ChargePointService()
    plug_share_service = PlugShareService()

    plug_share_service.save_stations_by_ids(station_ids=station_ids, steep_time=2)
    charge_point_service.save_stations_by_ids(station_ids=station_ids, steep_time=2)
