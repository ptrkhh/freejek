from typing import Optional, List

from pydantic import BaseModel

from entities.latlon import LatLon
from entities.web_api import Poi
from entities.web_trip import GetDriverResp, FareCalculatorReq


class RiderTripCurrent(BaseModel):
    last_count: int
    driver_location: Optional[LatLon]
    nearby_drivers: List[LatLon]
    driver_info: Optional[GetDriverResp]

    @classmethod
    def zero_value(cls):
        return cls(
            last_count=0,
            driver_location=None,
            nearby_drivers=[],
            driver_info=None,
        )


class RiderTripNew(BaseModel):
    last_count: int
    last_clicked: Optional[LatLon]
    search_results: List[Poi]
    search_query: Optional[str]
    last_search_query: Optional[str]
    pickup: LatLon
    dropoff: LatLon
    fare: int
    fare_req: Optional[FareCalculatorReq]
    path: List[LatLon]

    @classmethod
    def zero_value(cls, start_location: LatLon):
        return cls(
            last_count=0,
            last_clicked=None,
            search_results=[],
            search_query=None,
            last_search_query=None,
            pickup=start_location,
            dropoff=start_location,
            fare=0,
            fare_req=None,
            path=[]
        )
