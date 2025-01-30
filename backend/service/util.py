from math import radians, cos
from typing import Tuple

from backend.entities.latlon import LatLon


def minmaxlatlon(loc: LatLon, cluster_size_in_meters: int) -> Tuple[LatLon, LatLon]:
    distlat: float = cluster_size_in_meters / 111111.1  # 1 degree in meters
    minlat: float = loc.lat - distlat
    maxlat: float = loc.lat + distlat

    mindistlon: float = cluster_size_in_meters / (111111.1 * cos(radians(minlat)))
    minlon: float = loc.lon - mindistlon
    maxdistlon: float = cluster_size_in_meters / (111111.1 * cos(radians(maxlat)))
    maxlon: float = loc.lon + maxdistlon

    return LatLon(lat=minlat, lon=minlon), LatLon(lat=maxlat, lon=maxlon)
