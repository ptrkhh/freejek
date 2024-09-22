import uuid
from pydantic import BaseModel

class VehicleModel(BaseModel):
    id: uuid.UUID
    make: str
    model: str
    capacity: int
    _class: int
    created_at: datetime
    propulsion: str  # TODO enum
    type: str  # TODO enum
