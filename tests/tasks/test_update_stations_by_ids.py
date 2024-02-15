from httpx import Response

from src.tasks.update_stations_by_ids import update_stations_by_ids


def test_update_stations_by_ids(
    live_charge_api,
    charge_point_api,
    plug_share_api,
    charge_point_comments_api: callable,
    plug_share_info: dict,
    plug_share_comments: dict,
    charge_point_info: dict,
) -> None:
    # arrange
    station_id = 1

    live_charge_api(method='POST', uri='/api/v1/stations').mock(
        return_value=Response(200)
    )
    plug_share_api(method='POST', uri=f'/locations/{station_id}').mock(
        return_value=Response(200, json=plug_share_info)
    )
    charge_point_comments_api(method='POST', uri=f'/account/v1/driver/tip/{station_id}').mock(
        return_value=Response(200, json=plug_share_comments)
    )
    charge_point_api(method='POST', uri='/map-prod/v3/station/info').mock(
        return_value=Response(200, json=charge_point_info)
    )

    # act
    update_stations_by_ids(station_ids=[station_id])

    # assert
