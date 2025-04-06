import datetime
import uuid

from sqlmodel import Field, SQLModel


class LocationHistory(SQLModel, table=True):
    __tablename__ = "location_history"
    __table_args__ = {'extend_existing': True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )
    trip_id: uuid.UUID | None = Field(default=None, foreign_key="trip.id")
    driver_id: uuid.UUID | None = Field(default=None, foreign_key="driver.id")
    rider_id: uuid.UUID | None = Field(default=None, foreign_key="rider.id")

    lat: float
    lon: float
