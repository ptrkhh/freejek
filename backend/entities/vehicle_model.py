import datetime

from pydantic import UUID4, BaseModel, Field

from backend.entities.vehicle_unit import VehicleUnit


class VehicleModelBaseSchema(BaseModel):
    """VehicleModel Base Schema."""

    # Primary Keys
    id: UUID4

    # Columns
    capacity: int
    created_at: datetime.datetime
    field_class: int = Field(alias="class")
    field_type: str = Field(alias="type")
    make: str
    model: str
    propulsion: str


class VehicleModel(VehicleModelBaseSchema):
    """VehicleModel Schema for Pydantic.

    Inherits from VehicleModelBaseSchema. Add any customization here.
    """

    # Foreign Keys
    vehicle_unit: list[VehicleUnit] | None = Field(default=None)
