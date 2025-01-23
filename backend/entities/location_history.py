import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class LocationHistory(SQLModel, table=True):
    __tablename__ = "location_history"
    # __table_args__ = {'extend_existing': True}

    id: Optional[UUID] = Field(default=None, primary_key=True)
    created_at: Optional[datetime.datetime]
    trip_id: UUID | None = Field(default=None, foreign_key="trip.id")

    lat: float
    on: float
