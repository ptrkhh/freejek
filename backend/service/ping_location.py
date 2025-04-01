from uuid import UUID

from sqlmodel import Session

from backend.entities.driver import Driver
from backend.entities.rider import Rider
from data.latlon import LatLon
from backend.entities.location_history import LocationHistory
from backend.repository import Repository


class ServicePingLocation:
    def __init__(self, repository: Repository):
        self.repository = repository

    def ping_rider_location(self, loc: LatLon, email: str, trip_id: UUID = None,
                      session: Session = None) -> bool:
        rider: Rider = self.repository.rider.get_by_email(email)
        self.repository.location_history.insert_one(LocationHistory(
            lat=loc.lat,
            lon=loc.lon,
            rider_id=rider.id,
            trip_id=trip_id,
        ), session=session)


    def ping_driver_location(self, loc: LatLon, email: str, trip_id: UUID = None,
                      session: Session = None) -> bool:
        driver: Driver = self.repository.driver.get_by_email(email)
        self.repository.location_history.insert_one(LocationHistory(
            lat=loc.lat,
            lon=loc.lon,
            driver_id=driver.id,
            trip_id=trip_id,
        ), session=session)

