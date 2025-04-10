from math import radians, cos, sin, atan2, sqrt
from typing import List
from typing import Tuple

from pydantic import BaseModel


class LatLon(BaseModel):
    lat: float
    lon: float

    def as_list(self, reversed: bool = False) -> List[float]:
        return [self.lon, self.lat] if reversed else [self.lat, self.lon]

    def as_tuple(self, reversed: bool = False) -> Tuple[float, float]:
        return (self.lon, self.lat) if reversed else (self.lat, self.lon)

    def is_zero(self):
        return self.lat == 0.0 and self.lon == 0.0


def latlon_distance(loc1: LatLon, loc2: LatLon) -> float:
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = radians(loc1.lat), radians(loc1.lon), radians(loc2.lat), radians(loc2.lon)
    dlat, dlon = lat2 - lat1, lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371000 * c # earth radius * radian dist


def latlon_boundary_cluster(loc: LatLon, cluster_size_in_meters: int) -> Tuple[LatLon, LatLon]:
    distlat: float = cluster_size_in_meters / 111111.1  # 1 degree in meters
    minlat: float = loc.lat - distlat
    maxlat: float = loc.lat + distlat

    mindistlon: float = cluster_size_in_meters / (111111.1 * cos(radians(minlat)))
    minlon: float = loc.lon - mindistlon
    maxdistlon: float = cluster_size_in_meters / (111111.1 * cos(radians(maxlat)))
    maxlon: float = loc.lon + maxdistlon

    return LatLon(lat=minlat, lon=minlon), LatLon(lat=maxlat, lon=maxlon)
