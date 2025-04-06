import datetime
import uuid

from sqlmodel import Field, SQLModel


class VehicleUnit(SQLModel, table=True):
    __tablename__ = "vehicle_unit"
    __table_args__ = {'extend_existing': True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    vehicle_year: int
    vehicle_color: str
    license_plate: str
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
    photo_1: str | None = Field(default=None)
    photo_2: str | None = Field(default=None)
    photo_3: str | None = Field(default=None)
    driver_id: uuid.UUID = Field(foreign_key="driver.id")
    vehicle_id: uuid.UUID = Field(foreign_key="vehicle_model.id")
