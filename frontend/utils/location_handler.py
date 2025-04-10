import os
import time
import traceback
from time import sleep
from typing import Optional
from uuid import UUID

from streamlit_js_eval import get_geolocation

from backend.controller.router import Controller
from entities.latlon import LatLon, latlon_distance
from frontend.utils.token_handler import TokenHandler


class LocationHandler:
    def __init__(self, c: Controller, t: TokenHandler, location: Optional[LatLon] = None, permissive=False):
        self.c = c
        self.t = t
        self.current_location: LatLon = LatLon(lat=0, lon=0)
        if location and location.lat and location.lon:
            self.current_location = location
        else:
            self.update(timeout=30)  # allow longer timeout for initialization
        self.initial_location: LatLon = self.current_location
        self.last_update = time.time()
        self.ping_delay_idle = os.environ.get("PING_DELAY_IDLE", 15)
        self.ping_delay_active = os.environ.get("PING_DELAY_ACTIVE", 3)
        self.ping_delay_max = os.environ.get("PING_DELAY_MAX", 300)

    def update_initial_location(self):
        self.update()
        self.initial_location = self.current_location

    def update(self, trip_id: UUID = None, timeout: int = 10):
        try:
            location = get_geolocation()
            # {'coords': {'accuracy': 119, 'altitude': None, 'altitudeAccuracy': None, 'heading': None, 'latitude': -6.170324666666668, 'longitude': 106.79115449999998, 'speed': None}, 'timestamp': 1743616376830}
            finish_time = time.time() + timeout
            while (not location) and time.time() < finish_time:
                sleep(1)
            if not (location and "coords" in location):
                raise AssertionError("Could not find location")
            last_location = self.current_location
            self.current_location = LatLon(
                lat=location["coords"]["latitude"],
                lon=location["coords"]["longitude"]
            )
            if self.t.is_signed_in() and (not self.current_location.is_zero()):
                distance = latlon_distance(last_location, self.current_location)
                from_last_update = time.time() - self.last_update
                if from_last_update > self.ping_delay_max or distance > 10:
                    self.c.rider_ping_location(
                        loc=self.current_location,
                        email=self.t.get_email(),
                        trip_id=trip_id,
                    )
                    self.last_update = time.time()
        except Exception as e:
            print("ERROR UPDATE LOCATION", e)
            traceback.print_exc()
