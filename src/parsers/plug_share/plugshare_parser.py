import json
import logging
import os
import random
import time

import httpx


class PlugShareParser:
    __headers = {
        'Authorization': 'Basic d2ViX3YyOkVOanNuUE54NHhXeHVkODU=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    __base_url = "https://api.plugshare.com/v3/"
    __log_file = "plugshare_parser.log"

    def __init__(self):
        self.__create_logger()

    def get_locations_by_name(self, name: str):
        """
        :param name: The search query. Matches on name or address.
        """
        suffix_url = "locations/search"
        params = {"query": name,
                  }

        return self.__get_json(suffix_url, params)

    def get_locations_by_region(self, span_lat: float, span_lng: float, latitude: float, longitude: float, count=500):
        """
        :param span_lat: Latitude span in degrees of target search region.
        :param span_lng: Longitude span in degrees of target search region.
        :param latitude: Latitude coordinate of target search location.
        :param longitude: Longitude coordinate of target search location.
        :param count: Maximum count of locations to return. Count is capped at 500 regardless of specified value. 200-500 is a recommended value for most applications.
        """

        suffix_url = "locations/region"
        params = {"spanLat": span_lat,
                  "spanLng": span_lng,
                  "latitude": latitude,
                  "longitude": longitude,
                  "count": count,
                  }
        return self.__get_json(suffix_url, params)

    def get_location_by_id(self, location_id: int):
        suffix_url = f"locations/{location_id}"
        params = {}
        return self.__get_json(suffix_url, params)

    def __get_json(self, suffix_url: str, params: dict):
        response = httpx.get(url=self.__base_url + suffix_url, headers=self.__headers, params=params)
        if response.is_error:
            self.logger.info(response.status_code)
            return

        return response.json()

    @staticmethod
    def save_json_to_file(filename: str, json_data):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)

    def __create_logger(self):
        if os.path.exists(self.__log_file):
            os.remove(self.__log_file)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

        file_handler = logging.FileHandler(self.__log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.info("Plugshare Parser Log Initiated\n")


if __name__ == '__main__':
    parser = PlugShareParser()
    locations = parser.get_locations_by_region(11, 11, 37.5, -119.5)
    parser.save_json_to_file("locations.json", locations)

    count = 0
    for location in locations:
        time.sleep(random.randint(2, 5))
        location_id = location["id"]
        loc = parser.get_location_by_id(location_id)
        parser.save_json_to_file(f"location-{location_id}.json", loc)
        count += 1
        if count == 3:
            break
