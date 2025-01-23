import datetime
from typing import Optional
from uuid import UUID

from pydantic import UUID4, BaseModel, Field
from sqlmodel import SQLModel

from backend.entities.trip import Trip


class DisputeBaseSchema(BaseModel):

    # Columns
    closed_at: datetime.datetime | None = Field(default=None)
    driver_media_1: str | None = Field(default=None)
    driver_media_2: str | None = Field(default=None)
    driver_statement: str | None = Field(default=None)
    refunded_at: datetime.datetime | None = Field(default=None)
    rider_media_1: str | None = Field(default=None)
    rider_media_2: str | None = Field(default=None)
    rider_statement: str | None = Field(default=None)
    trip_id: UUID4


class Dispute(SQLModel, table=True):
    __tablename__ = "dispute"
    # __table_args__ = {'extend_existing': True}

    id: Optional[UUID] = Field(default=None, primary_key=True)
    trip_id: UUID = Field(foreign_key="trip.id")
    updated_at: datetime.datetime | None = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.datetime.now(datetime.timezone.utc)},
    )
    created_at: Optional[datetime.datetime]

    closed_at: datetime.datetime | None = Field(default=None)
    driver_media_1: str | None = Field(default=None)
    driver_media_2: str | None = Field(default=None)
    driver_statement: str | None = Field(default=None)
    refunded_at: datetime.datetime | None = Field(default=None)
    rider_media_1: str | None = Field(default=None)
    rider_media_2: str | None = Field(default=None)
    rider_statement: str | None = Field(default=None)
