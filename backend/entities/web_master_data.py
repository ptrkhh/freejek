import datetime
from uuid import UUID

from pydantic import BaseModel


class WebVehicleModel(BaseModel):
    id: UUID
    capacity: int
    created_at: datetime.datetime
    vehicle_class: int
    make: str
    model: str
    type: str
    propulsion: str
