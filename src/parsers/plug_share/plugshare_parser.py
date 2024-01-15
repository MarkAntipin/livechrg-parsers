import logging
import json
from typing import List, Optional

from settings import Settings
from utils.area import PlugShareArea
from utils.setup_logger import setup_logger
from utils.make_request import make_request
from utils.parse_area import parse_area

logger = logging.getLogger(__name__)
setup_logger(logger)

headers = {
    "Authorization": "Basic d2ViX3YyOkVOanNuUE54NHhXeHVkODU=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}

settings = Settings()


def get_locations(area: PlugShareArea) -> List[Optional[dict]] | None:
    params = {
        "spanLat": area.span_lat,
        "spanLng": area.span_lng,
        "latitude": area.latitude,
        "longitude": area.longitude,
        "count": 1000,
    }

    response = make_request(
        url=settings.PLUGSHARE_LOCATIONS_URL,
        params=params,
        headers=headers
    )
    if response is None:
        return
    return response.json()


def get_comments(location_id: int) -> List[Optional[dict]] | None:
    response = make_request(
        url=settings.PLUGSHARE_COMMENT_URL.format(location_id=location_id),
        headers=headers
    )
    if response is None:
        return
    return response.json()


def save_json_file(filename: str, json_data: List[dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    search_area = PlugShareArea(span_lat=1, span_lng=1, latitude=37.5, longitude=-119.5)
    locations = parse_area(area=search_area, api_cap=250, get_locations_func=get_locations)
    comments = []
    for location in locations:
        comments.append(get_comments(location["id"]))
    print(comments)
