from typing import List
from typing import List
from uuid import UUID

from sqlmodel import Session

from backend.entities.latlon import LatLon
from backend.entities.trip import Trip
from backend.entities.web_trip import GetTripsResp
from backend.repository import Repository
from backend.service.util import minmaxlatlon


class ServiceDriverTrip:
    def __init__(self, repository: Repository):
        self.repository = repository

    def list_trips(self, loc: LatLon, radius_in_m: int, page: int, limit: int, session: Session = None) -> List[
        GetTripsResp]:  # TODO page
        minlatlon, maxlatlon = minmaxlatlon(loc=loc, cluster_size_in_meters=radius_in_m)
        trips = self.repository.trip.get_by_pickup_region(
            minlatlon=minlatlon,
            maxlatlon=maxlatlon,
            # TODO status
            session=session,
        )
        return [GetTripsResp(
            id=i.id,
            accepted_at=i.accepted_at,
            canceled_at=i.canceled_at,
            comment_to_driver=i.comment_to_driver,
            comment_to_rider=i.comment_to_rider,
            completed_at=i.completed_at,
            created_at=i.created_at,
            dropoff=LatLon(lat=i.dropoff_lat, lon=i.dropoff_lon),
            fare=i.fare,
            passenger=i.passenger,
            pickup=LatLon(lat=i.pickup_lat, lon=i.pickup_lon),
            rate_to_driver=i.rate_to_driver,
            rate_to_rider=i.rate_to_rider,
            request=i.request,
            started_at=i.started_at,
            updated_at=i.updated_at,
            vehicle_color=i.vehicle_color,
            vehicle_plate=i.vehicle_plate,
            driver_id=i.driver_id,
            rider_id=i.rider_id,
            vehicle_id=i.vehicle_id,
        ) for i in trips]

    def accept_trip(self, driver_id: UUID, trip_id: UUID, session: Session = None) -> Trip:
        # TODO check driver is not currently in any other trip
        # TODO check trip is eligible to accept
        # TODO accept
        raise NotImplementedError

    def complete_trip(self, driver_id: UUID, trip_id: UUID, session: Session = None) -> Trip:
        # TODO check trip is eligible to complete
        # TODO complete
        raise NotImplementedError
