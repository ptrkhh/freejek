import datetime
import uuid
from enum import Enum

from sqlmodel import SQLModel, Field


class VehicleModel(SQLModel, table=True):
    __tablename__ = "vehicle_model"
    __table_args__ = {'extend_existing': True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    capacity: int
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )
    vehicle_class: int
    make: str
    model: str

    class VehicleType(Enum):
        CAR = "CAR"
        MOTORCYCLE = "MOTORCYCLE"

    type: VehicleType

    class VehiclePropulsion(Enum):
        PETROL = "PETROL"
        HYBRID = "HYBRID"
        ELECTRIC = "ELECTRIC"
        DIESEL = "DIESEL"

    propulsion: VehiclePropulsion
