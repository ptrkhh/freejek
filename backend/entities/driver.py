import datetime
import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class Driver(SQLModel, table=True):
    __tablename__ = "driver"
    __table_args__ = {'extend_existing': True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    deleted_at: datetime.datetime | None = Field(default=None)
    updated_at: datetime.datetime | None = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.datetime.now(datetime.timezone.utc)},
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )
    auth_id: uuid.UUID | None = Field(default=None)
    email: str | None = Field(default=None)
    last_active: Optional[datetime.datetime]
    last_deactive: datetime.datetime | None = Field(default=None)
    license_number: str | None = Field(default=None)
    name: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    photo_id: str | None = Field(default=None)
    photo_id_verification: str | None = Field(default=None)
    photo_profile: str | None = Field(default=None)
    verified_at: datetime.datetime | None = Field(default=None)
