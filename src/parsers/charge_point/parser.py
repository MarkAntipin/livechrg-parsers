"""Parser for https://driver.chargepoint.com"""

import httpx
from pprint import pprint
from functions import make_params_string

# links that used in scraping or can be useful in the future
MAIN_PAGE_LINK = "https://driver.chargepoint.com"
STATION_LIST_LINK_BEGIN = "https://mc.chargepoint.com/map-prod/v2"
STATION_INFO_LINK_BEGIN = "https://mc.chargepoint.com/map-prod/v3/station/info"
TIPS_LINK_BEGIN = "https://account.chargepoint.com/account/v1/driver/tip/"

# попытка передать параметры в таком виде напрямую приводит к выводу ошибки java.lang.NullPointerException вместо
# списка станций. Предполагаю, что это как то связано с необычным способом передачи параметров запроса, используемом
# на сайте (?{} вместо ?key=value)
params_for_station_list_request = {
    "station_list": {
        "screen_width": 857.5999755859375,
        "screen_height": 536,
        "ne_lat": 45.99248923039967,
        "ne_lon": -97.28690881274578,
        "sw_lat": 27.268439039977505,
        "sw_lon": -134.9919869377458,
        "page_size": 10,  # number of stations to be scraped
        "page_offset": "",
        "sort_by": "distance",
        "reference_lat": 37.20770443804854,
        "reference_lon": -116.13944787524578,
        "include_map_bound": True,
        "filter": {
            "price_free": False,
            "status_available": False,
            "dc_fast_charging": False,
            "network_chargepoint": False,
            "connector_l1": False,
            "connector_l2": False,
            "connector_l2_nema_1450": False,
            "connector_l2_tesla": False,
            "connector_chademo": False,
            "connector_combo": False,
            "connector_tesla": False,
        },
        "bound_output": True,
    }
}

params_string_for_station_list_request = make_params_string(
    params_for_station_list_request
)
stations_info_response = httpx.get(
    STATION_LIST_LINK_BEGIN + "?" + params_string_for_station_list_request
)

stations_info = {}
for station in stations_info_response.json()["station_list"]["stations"]:
    station_id = station["device_id"]
    stations_info[station_id] = station
    query_params = {"deviceId": station_id}
    station_info_response = httpx.get(STATION_INFO_LINK_BEGIN, params=query_params)
    stations_info[station_id].update(station_info_response.json())
    tips_response = httpx.get(TIPS_LINK_BEGIN + str(station_id))
    stations_info[station_id]["tips"] = tips_response.json()

pprint(stations_info)
