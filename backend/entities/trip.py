import datetime
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from backend.entities.latlon import LatLon


class Trip(SQLModel, table=True):
    __tablename__ = "trip"
    # __table_args__ = {'extend_existing': True}

    id: Optional[UUID] = Field(default=None, primary_key=True)

    accepted_at: datetime.datetime | None = Field(default=None)
    canceled_at: datetime.datetime | None = Field(default=None)
    comment_to_driver: str | None = Field(default=None)
    comment_to_rider: str | None = Field(default=None)
    completed_at: datetime.datetime | None = Field(default=None)
    created_at: datetime.datetime
    dropoff_lat: float
    dropoff_lon: float
    fare: int
    passenger: int
    pickup_lat: float
    pickup_lon: float
    rate_to_driver: int | None = Field(default=None)
    rate_to_rider: int | None = Field(default=None)
    request: str | None = Field(default=None)
    started_at: datetime.datetime | None = Field(default=None)
    updated_at: datetime.datetime | None = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.datetime.now(datetime.timezone.utc)},
    )
    vehicle_color: str
    vehicle_plate: str

    driver_id: UUID | None = Field(default=None, foreign_key="driver.id")
    rider_id: UUID = Field(foreign_key="rider.id")
    vehicle_id: UUID | None = Field(default=None, foreign_key="vehicle_unit.id")

class TripCreationRequest(BaseModel):
    rider_id: UUID
    orig: LatLon
    dest: LatLon
    vehicle_class: int
    vehicle_type: Literal["car", "motorcycle"]
    request: str
    passenger: int
    fare: int