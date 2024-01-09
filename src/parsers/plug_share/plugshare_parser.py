import json
from typing import List, Optional

from utils.logger import create_logger
from utils.make_request import make_request
from utils.base_urls import BaseUrl

logger = create_logger()

headers = {
    "Authorization": "Basic d2ViX3YyOkVOanNuUE54NHhXeHVkODU=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}

base_url = BaseUrl.PLUGSHARE.value


def get_locations_by_name(name: str) -> List[Optional[dict]] | None:
    """
    :param name: The search query. Matches on name or address.
    """
    suffix_url = "locations/search"
    params = {"query": name}

    return make_request(f"{base_url}/{suffix_url}", params=params, headers=headers).json()


def rec_get_locations_by_region(
        span_lat: float,
        span_lng: float,
        latitude: float,
        longitude: float,
) -> List[Optional[dict]] | None:
    result = get_locations_by_region(span_lat, span_lng, latitude, longitude)

    if len(result) < 250:
        return result

    else:
        new_span_tuple = (span_lat / 2, span_lng / 2,)

        upper_left_center = (latitude + span_lat / 4, longitude - span_lat / 4,)
        upper_right_center = (latitude + span_lat / 4, longitude + span_lat / 4,)
        bottom_left_center = (latitude - span_lat / 4, longitude - span_lat / 4,)
        bottom_right_center = (latitude - span_lat / 4, longitude + span_lat / 4,)

        all_locations = [
            *get_locations_by_region(*new_span_tuple, *upper_left_center),
            *get_locations_by_region(*new_span_tuple, *upper_right_center),
            *get_locations_by_region(*new_span_tuple, *bottom_left_center),
            *get_locations_by_region(*new_span_tuple, *bottom_right_center),
        ]

        # locations are filtered to avoid duplication (not necessarily present)
        unique_locations = []
        unique_ids = set()

        for location in all_locations:
            loc_id = location["id"]
            if loc_id in unique_ids:
                pass
            else:
                unique_ids.add(loc_id)
                unique_locations.append(location)

        return unique_locations


def get_locations_by_region(
        span_lat: float,
        span_lng: float,
        latitude: float,
        longitude: float,
) -> List[Optional[dict]] | None:
    """
    :param span_lat: Latitude span in degrees of target search region.
    :param span_lng: Longitude span in degrees of target search region.
    :param latitude: Latitude coordinate of target search location.
    :param longitude: Longitude coordinate of target search location.
    """

    suffix_url = "locations/region"
    params = {
        "spanLat": span_lat,
        "spanLng": span_lng,
        "latitude": latitude,
        "longitude": longitude,
        "count": 1000,
    }
    return make_request(f"{base_url}/{suffix_url}", params=params, headers=headers).json()


def get_location_by_id(location_id: int) -> List[Optional[dict]] | None:
    suffix_url = f"locations/{location_id}"
    params = {}
    return make_request(f"{base_url}/{suffix_url}", params=params, headers=headers).json()


def save_json_file(filename: str, json_data: dict | List[dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    locations = get_locations_by_region(2, 2, 37.5, -119.5)
    save_json_file("some.json", locations)
    print(len(locations))
    locations = rec_get_locations_by_region(2, 2, 37.5, -119.5)
    save_json_file("other.json", locations)
    print(len(locations))
