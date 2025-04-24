from typing import Optional, List

from pydantic import BaseModel

from entities.latlon import LatLon
from entities.web_api import Poi
from entities.web_trip import GetDriverResp


class RiderTripCurrent(BaseModel):
    last_count: int
    driver_location: Optional[LatLon]
    nearby_drivers: List[LatLon]
    driver_info: Optional[GetDriverResp]

class RiderTripNew(BaseModel):
    last_count: int
    last_clicked: Optional[LatLon]
    search_results: List[Poi]
    search_query: Optional[str]
    last_search_query: Optional[str]
    pickup: LatLon
    dropoff: LatLon
    fare: int
    fare_pickup: Optional[LatLon]
    fare_dropoff: Optional[LatLon]
