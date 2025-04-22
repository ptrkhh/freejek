from typing import Union, List
from uuid import UUID

from backend.controller.router import Controller
from entities.latlon import LatLon
from entities.web_trip import GetTripResp, GetDriverResp
from frontend.utils.token_handler import TokenHandler


class TripHandler:
    def __init__(self, c: Controller, t: TokenHandler):
        self.c = c
        self.t = t
        self.last_trip: Union[GetTripResp, None] = self.update()
        self.route_path: List[LatLon] = []

    def update(self) -> Union[GetTripResp, None]:
        self.last_trip = self.c.rider_get_latest_trip(self.t.get_token())
        start, end = self.last_trip.pickup, self.last_trip.dropoff
        if (not self.route_path) or self.route_path[0] != start or self.route_path[-1] != end:
            self.route_path = []
        return self.last_trip

    def get_last_trip(self):
        if not self.last_trip:
            self.update()
        return self.last_trip

    def get_driver(self) -> Union[GetDriverResp, None]:
        if self.last_trip is None:
            return None
        return self.c.rider_get_driver(self.last_trip.driver_id)

    def get_route_path(self) -> List[LatLon]:
        if not self.route_path:
            route_path = self.c.rider_get_trip_path(self.last_trip.pickup, self.last_trip.dropoff)
            self.route_path = [self.get_last_trip().pickup] + route_path + [self.get_last_trip().dropoff]
        return self.route_path

    def rate_driver(self, rider_id: UUID, trip_id: UUID, stars: int, note: str) -> None:
        self.c.rider_rate_driver(
            rider_id=rider_id,
            trip_id=trip_id,
            stars=stars,
            note=note,
        )
