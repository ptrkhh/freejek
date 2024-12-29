import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.trip import Trip


class LocationHistoryBaseSchema(BaseModel):
    """LocationHistory Base Schema."""

    # Primary Keys
    id: UUID4

    # Columns
    created_at: datetime.datetime
    lat: float
    on: float
    trip_id: UUID4


class LocationHistory(LocationHistoryBaseSchema):
    """LocationHistory Schema for Pydantic.

    Inherits from LocationHistoryBaseSchema. Add any customization here.
    """

    # Foreign Keys
    trip: list[Trip] | None = Field(default=None)
