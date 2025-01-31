import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


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


def trip_status(trip: Trip) -> str:  # TODO ENUM
    if trip.canceled_at:
        return "CANCELED"
    if trip.completed_at:
        return "COMPLETED"
    if trip.started_at:
        return "STARTED"
    if trip.accepted_at:
        return "ACCEPTED"
    return "PENDING"


def is_trip_active(trip: Trip) -> bool:
    status = trip_status(trip)
    return status == "ACCEPTED" or status == "PENDING" or status == "STARTED"
