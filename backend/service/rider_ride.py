import uuid
from typing import Literal

from backend.entities.latlon import LatLon
from backend.entities.trip import TripCreationRequest
from backend.repository import Repository


class ServiceRiderRide:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.base_price: int = 5000
        self.distance_price_per_km: int = 5000
        self.vehicle_class_modifier: float = 1.5
        self.vehicle_type_modifier: float = 2.0

    def fare_calculator(self, orig: LatLon, dest: LatLon, vehicle_class: int,
                        vehicle_type: Literal["car", "motorcycle"]) -> int:
        distance_in_m: int = 123  # TODO
        base_price = self.base_price + int((self.distance_price_per_km * distance_in_m) / 1000)
        vehicle_type_modifier: float = self.vehicle_type_modifier if vehicle_type == "car" else 1.0
        vehicle_class_modifier: float = self.vehicle_class_modifier * vehicle_class  # TODO plus one?
        # TODO surge pricing
        return int(base_price * vehicle_class_modifier * vehicle_type_modifier)

    def request_trip(self, req: TripCreationRequest) -> uuid.UUID:
        # TODO get Rider
        # TODO calculate fare
        # TODO insert to trip
        trip_id = uuid.uuid4() # TODO
        return trip_id

