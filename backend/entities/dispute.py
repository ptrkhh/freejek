import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.trip import Trip


class DisputeBaseSchema(BaseModel):
    # Primary Keys
    id: UUID4

    # Columns
    closed_at: datetime.datetime | None = Field(default=None)
    created_at: datetime.datetime
    driver_media_1: str | None = Field(default=None)
    driver_media_2: str | None = Field(default=None)
    driver_statement: str | None = Field(default=None)
    refunded_at: datetime.datetime | None = Field(default=None)
    rider_media_1: str | None = Field(default=None)
    rider_media_2: str | None = Field(default=None)
    rider_statement: str | None = Field(default=None)
    trip_id: UUID4
    updated_at: datetime.datetime | None = Field(default=None)


class Dispute(DisputeBaseSchema):
    trip: list[Trip] | None = Field(default=None)
