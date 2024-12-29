import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.trip import Trip
from backend.entities.vehicle_unit import VehicleUnit


class DriverBaseSchema(BaseModel):
    # Primary Keys
    id: UUID4

    # Columns
    auth_id: UUID4
    created_at: datetime.datetime | None = Field(default=None)
    deleted_at: datetime.datetime | None = Field(default=None)
    email: UUID4 | None = Field(default=None)
    last_active: datetime.datetime
    last_deactive: datetime.datetime | None = Field(default=None)
    license_number: str | None = Field(default=None)
    name: str | None = Field(default=None)
    phone: UUID4 | None = Field(default=None)
    photo_id: str | None = Field(default=None)
    photo_id_verification: str | None = Field(default=None)
    photo_profile: str | None = Field(default=None)
    updated_at: datetime.datetime | None = Field(default=None)
    verified_at: datetime.datetime | None = Field(default=None)


class Driver(DriverBaseSchema):
    """Driver Schema for Pydantic.

    Inherits from DriverBaseSchema. Add any customization here.
    """

    # Foreign Keys
    trip: list[Trip] | None = Field(default=None)
    vehicle_unit: list[VehicleUnit] | None = Field(default=None)
