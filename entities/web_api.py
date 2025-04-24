from pydantic import BaseModel

from entities.latlon import LatLon


class Poi(BaseModel):
    location: LatLon
    name: str
    street: str
    postal_code: str
