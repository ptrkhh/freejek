import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

import uuid

class Rider(SQLModel, table=True):
    __tablename__ = "rider"
    __table_args__ = {'extend_existing': True}

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

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

    auth_id: UUID | None = Field(default=None)

    email: str | None = Field(default=None)
    name: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    photo: str | None = Field(default=None)
