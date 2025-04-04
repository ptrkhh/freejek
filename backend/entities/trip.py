import datetime
from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID


class Trip(SQLModel, table=True):
    __tablename__ = "trip"
    __table_args__ = {'extend_existing': True}

    id: Optional[UUID] = Field(default=None, primary_key=True)

    accepted_at: datetime.datetime | None = Field(default=None)
    canceled_at: datetime.datetime | None = Field(default=None)
    comment_from_driver: str | None = Field(default=None)
    comment_from_rider: str | None = Field(default=None)
    completed_at: datetime.datetime | None = Field(default=None)
    created_at: datetime.datetime
    dropoff_lat: float
    dropoff_lon: float
    fare: int
    passenger: int
    pickup_lat: float
    pickup_lon: float
    rate_from_driver: int | None = Field(default=None)
    rate_from_rider: int | None = Field(default=None)
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
