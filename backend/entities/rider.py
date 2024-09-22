import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.trip import Trip


class RiderBaseSchema(BaseModel):
    """Rider Base Schema."""

    # Primary Keys
    id: UUID4

    # Columns
    auth_id: UUID4 | None = Field(default=None)
    created_at: datetime.datetime
    deleted_at: datetime.datetime | None = Field(default=None)
    email: str | None = Field(default=None)
    name: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    photo: str | None = Field(default=None)
    updated_at: datetime.datetime


class Rider(RiderBaseSchema):
    """Rider Schema for Pydantic.

    Inherits from RiderBaseSchema. Add any customization here.
    """

    # Foreign Keys
    trip: list[Trip] | None = Field(default=None)
