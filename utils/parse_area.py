import typing

from utils.area import Area


def parse_area(*, area: Area, api_cap: int, get_locations_func: typing.Callable) -> list:
    stack = [area]

    all_locations = []
    while stack:
        area = stack.pop()
        locations = get_locations_func(area=area)
        if len(locations) < api_cap:
            all_locations.extend(locations)
        else:
            areas = area.split()
            stack.extend(areas)

    return all_locations

