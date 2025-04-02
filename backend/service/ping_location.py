from typing import List
from uuid import UUID

from sqlmodel import Session

from backend.entities.driver import Driver
from backend.entities.location_history import LocationHistory
from backend.entities.rider import Rider
from backend.repository import Repository
from backend.service.util import minmaxlatlon
from data.latlon import LatLon


class ServicePingLocation:
    def __init__(self, repository: Repository):
        self.repository = repository

    def ping_rider_location(self, loc: LatLon, email: str, trip_id: UUID = None,
                            session: Session = None) -> None:
        rider: Rider = self.repository.rider.get_by_email(email)
        self.repository.location_history.insert_one(LocationHistory(
            lat=loc.lat,
            lon=loc.lon,
            rider_id=rider.id,
            trip_id=trip_id,
        ), session=session)

    def ping_driver_location(self, loc: LatLon, email: str, trip_id: UUID = None,
                             session: Session = None) -> None:
        driver: Driver = self.repository.driver.get_by_email(email)
        self.repository.location_history.insert_one(LocationHistory(
            lat=loc.lat,
            lon=loc.lon,
            driver_id=driver.id,
            trip_id=trip_id,
        ), session=session)

    def fetch_driver_location(self, driver_id: UUID, timeout: int = 300, session: Session = None) -> List[LatLon]:
        locations: List[LocationHistory] = self.repository.location_history.get_by_driver_id(
            driver_id=driver_id,
            timeout=timeout,
            session=session,
        )
        return [LatLon(lat=i.lat, lon=i.lon) for i in locations] if locations else []

    def fetch_nearby_drivers(self, loc: LatLon, radius: int = 1000, timeout: int = 300, session: Session = None) -> List[LatLon]:
        locmin, locmax = minmaxlatlon(loc, radius)
        locations: List[LocationHistory] = self.repository.location_history.fetch_nearby_drivers(
            locmin=locmin,
            locmax=locmax,
            timeout=timeout,
            session=session,
        )
        return [LatLon(lat=i.lat, lon=i.lon) for i in locations] if locations else []
