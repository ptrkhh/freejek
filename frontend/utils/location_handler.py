import traceback
from uuid import UUID, uuid4

from streamlit_js_eval import get_geolocation

from backend.controller.router import Controller
from data.latlon import LatLon
from frontend.utils.token_handler import TokenHandler


class LocationHandler:
    def __init__(self, c: Controller, t: TokenHandler, location: LatLon = None, permissive=False):
        self.c = c
        self.t = t
        self.current_location = None
        self.update()
        # if not location:
        #     location = get_geolocation()
        #     while not (permissive or (location and location["coords"] and location["coords"]["latitude"])):
        #         location = get_geolocation()
        self.initial_location = self.current_location
        # self.current_location = location

    def update_initial_location(self):
        self.update()
        self.initial_location = self.current_location

    def update(self, trip_id: UUID = None):
        try:
            location = get_geolocation()
            # {'coords': {'accuracy': 119, 'altitude': None, 'altitudeAccuracy': None, 'heading': None, 'latitude': -6.170324666666668, 'longitude': 106.79115449999998, 'speed': None}, 'timestamp': 1743616376830}
            if not (location and location["coords"] and location["coords"]["latitude"]):
                return
            self.current_location = LatLon(
                lat=location["coords"]["latitude"],
                lon=location["coords"]["longitude"]
            )
            if self.t.is_signed_in():
                self.c.rider_ping_location(
                    loc=location,
                    email=self.t.get_email(),
                    trip_id=trip_id,
                )
        except Exception as e:
            print("ERROR UPDATE LOCATION", e)
            traceback.print_exc()
