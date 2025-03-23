import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field


class VehicleModel(SQLModel, table=True):
    __tablename__ = "vehicle_model"
    __table_args__ = {'extend_existing': True}

    id: Optional[UUID] = Field(default=None, primary_key=True)
    print("ID GENERATED")
    capacity: int
    created_at: Optional[datetime.datetime]
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
