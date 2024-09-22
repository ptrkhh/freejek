import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.dispute import Dispute
from backend.entities.driver import Driver
from backend.entities.location_history import LocationHistory
from backend.entities.rider import Rider
from backend.entities.vehicle_unit import VehicleUnit


class TripBaseSchema(BaseModel):
    """Trip Base Schema."""

    # Primary Keys
    id: UUID4

    # Columns
    accepted_at: datetime.datetime | None = Field(default=None)
    canceled_at: datetime.datetime | None = Field(default=None)
    comment_to_driver: str | None = Field(default=None)
    comment_to_rider: str | None = Field(default=None)
    completed_at: datetime.datetime | None = Field(default=None)
    created_at: datetime.datetime
    driver_id: UUID4
    dropoff_lat: float
    dropoff_lon: float
    fare: int
    passenger: int
    pickup_lat: float
    pickup_lon: float
    rate_to_driver: int | None = Field(default=None)
    rate_to_rider: int | None = Field(default=None)
    request: str | None = Field(default=None)
    rider_id: UUID4
    started_at: datetime.datetime | None = Field(default=None)
    updated_at: datetime.datetime | None = Field(default=None)
    vehicle_color: str
    vehicle_id: UUID4
    vehicle_plate: str


class Trip(TripBaseSchema):
    """Trip Schema for Pydantic.

    Inherits from TripBaseSchema. Add any customization here.
    """

    # Foreign Keys
    driver: list[Driver] | None = Field(default=None)
    rider: list[Rider] | None = Field(default=None)
    vehicle_unit: list[VehicleUnit] | None = Field(default=None)
    dispute: list[Dispute] | None = Field(default=None)
    location_history: list[LocationHistory] | None = Field(default=None)
