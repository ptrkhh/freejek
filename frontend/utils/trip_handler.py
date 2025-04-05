from typing import Union

from backend.controller.router import Controller
from entities.web_trip import GetTripResp
from frontend.utils.token_handler import TokenHandler


class TripHandler:
    def __init__(self, c: Controller, t: TokenHandler):
        self.c = c
        self.t = t
        self.last_trip = self.update()

    def update(self) -> Union[GetTripResp, None]:
        self.last_trip = self.c.rider_get_latest_trip(self.t.get_token())
        return self.last_trip
