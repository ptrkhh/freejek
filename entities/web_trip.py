import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from entities.latlon import LatLon
from entities.trip_status import TripStatus


class TripCreationReq(BaseModel):
    auth_id: UUID
    pickup: LatLon
    dropoff: LatLon
    vehicle_class: int
    vehicle_type: Literal["CAR", "MOTORCYCLE"]
    request: str
    passenger: int
    fare: int


class GetTripsResp(BaseModel):
    id: UUID

    accepted_at: datetime.datetime | None
    canceled_at: datetime.datetime | None
    comment_to_driver: str | None
    comment_to_rider: str | None
    completed_at: datetime.datetime | None
    created_at: datetime.datetime
    dropoff: LatLon
    fare: int
    passenger: int
    pickup: LatLon
    rate_to_driver: int | None
    rate_to_rider: int | None
    request: str | None
    started_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    vehicle_color: str | None
    vehicle_plate: str | None
    vehicle_make: str | None
    vehicle_model: str | None

    driver_id: UUID | None
    rider_id: UUID
    vehicle_id: UUID | None


class GetTripResp(BaseModel):
    id: UUID

    accepted_at: datetime.datetime | None
    canceled_at: datetime.datetime | None
    comment_to_driver: str | None
    comment_to_rider: str | None
    completed_at: datetime.datetime | None
    created_at: datetime.datetime
    dropoff: LatLon
    fare: int
    passenger: int
    pickup: LatLon
    rate_to_driver: int | None
    rate_to_rider: int | None
    request: str | None
    started_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    vehicle_color: str | None
    vehicle_plate: str | None
    vehicle_make: str | None
    vehicle_model: str | None

    driver_id: UUID | None
    rider_id: UUID
    vehicle_id: UUID | None

    status: TripStatus

class GetDriverResp(BaseModel):
    id: UUID
    updated_at: datetime.datetime | None
    created_at: datetime.datetime
    last_active: datetime.datetime | None
    last_deactive: datetime.datetime | None
    name: str | None
    phone: str | None
    photo_profile: str | None

class FareCalculatorReq(BaseModel):
    orig: LatLon
    dest: LatLon
    vehicle_class: int
    vehicle_type: Literal["CAR", "MOTORCYCLE"]
