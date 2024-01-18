import abc
from typing import List

from pydantic import BaseModel


class Area(abc.ABC):
    @abc.abstractmethod
    def split(self) -> List:
        pass


class PlugShareArea(Area, BaseModel):
    span_lat: float
    span_lng: float
    latitude: float
    longitude: float

    def split(self, n: int = 2) -> List["PlugShareArea"]:

        sub_area_width = self.span_lng / n
        sub_area_height = self.span_lat / n

        sub_areas = []

        for i in range(n):
            for j in range(n):
                sub_area = PlugShareArea(
                    longitude=self.longitude + ((i - (n - 1) / 2) * sub_area_width),
                    latitude=self.latitude + ((j - (n - 1) / 2) * sub_area_height),
                    span_lat=sub_area_height,
                    span_lng=sub_area_width
                )
                sub_areas.append(sub_area)
        return sub_areas


class ChargePointArea(Area, BaseModel):
    sw_lon: float
    sw_lat: float
    ne_lon: float
    ne_lat: float

    def split(self, divisor: int = 2) -> list['ChargePointArea']:
        lon_span = self.ne_lon - self.sw_lon
        lat_span = self.ne_lat - self.sw_lat
        sub_area_width = lon_span / divisor
        sub_area_height = lat_span / divisor
        sub_areas = []

        for i in range(divisor):
            for j in range(divisor):
                sub_area = ChargePointArea(
                    sw_lon = self.sw_lon + (j * sub_area_width),
                    sw_lat = self.sw_lat + (i * sub_area_height),
                    ne_lon = self.sw_lon + ((j + 1) * sub_area_width),
                    ne_lat = self.sw_lat + ((i + 1) * sub_area_height),
                )
                sub_areas.append(sub_area)

        return sub_areas
