import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.driver import Driver
from backend.entities.trip import Trip
from models import VehicleModel


class VehicleUnitBaseSchema(BaseModel):
    """VehicleUnit Base Schema."""

    # Primary Keys
    id: UUID4

    # Columns
    created_at: datetime.datetime
    deleted_at: datetime.datetime | None = Field(default=None)
    driver_id: UUID4
    license_plate: str
    photo_1: str | None = Field(default=None)
    photo_2: str | None = Field(default=None)
    photo_3: str | None = Field(default=None)
    updated_at: datetime.datetime | None = Field(default=None)
    vehicle_color: str
    vehicle_id: UUID4
    vehicle_year: int


class VehicleUnit(VehicleUnitBaseSchema):
    """VehicleUnit Schema for Pydantic.

    Inherits from VehicleUnitBaseSchema. Add any customization here.
    """

    # Foreign Keys
    driver: list[Driver] | None = Field(default=None)
    vehicle_model: list[VehicleModel] | None = Field(default=None)
    trip: list[Trip] | None = Field(default=None)
