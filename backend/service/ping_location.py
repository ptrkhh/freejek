from uuid import UUID

from sqlmodel import Session

from data.latlon import LatLon
from backend.entities.location_history import LocationHistory
from backend.repository import Repository


class ServicePingLocation:
    def __init__(self, repository: Repository):
        self.repository = repository

    def ping_location(self, loc: LatLon, driver_id: UUID = None, rider_id: UUID = None, trip_id: UUID = None,
                      session: Session = None) -> bool:  # TODO page
        if driver_id is None and rider_id is None:
            raise AssertionError("MUST PROVIDE DRIVER ID OR RIDER ID")

        self.repository.location_history.insert_one(LocationHistory(
            lat=loc.lat,
            lon=loc.lon,
            driver_id=driver_id,
            rider_id=rider_id,
            trip_id=trip_id,
        ), session=session)
