import logging
from datetime import datetime
from typing import List
from uuid import UUID

from sqlmodel import Session

from entities.latlon import LatLon, latlon_boundary_cluster
from entities.trip_status import TripStatus, trip_status
from entities.web_trip import GetTripsResp
from backend.repository import Repository


class ServiceDriverTrip:
    def __init__(self, repository: Repository):
        self.repository = repository

    def list_trips(self, loc: LatLon, radius_in_m: int, session: Session = None) -> List[
        GetTripsResp]:  # TODO page
        minlatlon, maxlatlon = latlon_boundary_cluster(loc=loc, cluster_size_in_meters=radius_in_m)
        trips = self.repository.trip.get_by_pickup_region(
            minlatlon=minlatlon,
            maxlatlon=maxlatlon,
            # TODO page limit
            session=session,
        )
        return [GetTripsResp(
            id=i.id,
            accepted_at=i.accepted_at,
            canceled_at=i.canceled_at,
            comment_from_driver=i.comment_from_driver,
            comment_from_rider=i.comment_from_rider,
            completed_at=i.completed_at,
            created_at=i.created_at,
            dropoff=LatLon(lat=i.dropoff_lat, lon=i.dropoff_lon),
            fare=i.fare,
            passenger=i.passenger,
            pickup=LatLon(lat=i.pickup_lat, lon=i.pickup_lon),
            rate_from_driver=i.rate_from_driver,
            rate_from_rider=i.rate_from_rider,
            request=i.request,
            started_at=i.started_at,
            updated_at=i.updated_at,
            vehicle_color=i.vehicle_color,
            vehicle_plate=i.vehicle_plate,
            driver_id=i.driver_id,
            rider_id=i.rider_id,
            vehicle_id=i.vehicle_id,
        ) for i in trips]

    def accept_trip(self, trip_id: UUID, driver_id: UUID, vehicle_id: UUID, session: Session = None) -> None:
        trip = self.repository.trip.get_by_id(trip_id, session=session)
        status = trip_status(trip)
        if status != TripStatus.AVAILABLE:
            raise AssertionError(f"TRIP {trip_id} STATUS {status} IS NOT AVAILABLE")
        other_trips = self.repository.trip.get_by_driver_id(driver_id, TripStatus.ONGOING, session=session)
        if len(other_trips) > 0:
            raise AssertionError(f"DRIVER {driver_id} IN ANOTHER TRIP")
        vehicle_unit = self.repository.vehicle_unit.get_by_id(vehicle_id, session=session)
        vehicle_model = self.repository.vehicle_model.get_by_id(vehicle_unit.vehicle_id, session=session)
        trip.accepted_at = datetime.now()
        trip.driver_id = driver_id
        trip.vehicle_id = vehicle_id
        trip.vehicle_color = vehicle_unit.color
        trip.vehicle_plate = vehicle_unit.plate
        trip.vehicle_make = vehicle_model.make
        trip.vehicle_model = vehicle_model.model
        self.repository.trip.update(trip, session=session)

    def complete_trip(self, trip_id: UUID, driver_id: UUID, session: Session = None) -> None:
        trip = self.repository.trip.get_by_id(trip_id, session=session)
        if trip.driver_id != driver_id:
            raise AssertionError(f"TRIP {trip_id} IS NOT DRIVER {driver_id}")
        status = trip_status(trip)
        if status != TripStatus.ONGOING:
            raise AssertionError(f"TRIP {trip_id} STATUS {status} IS NOT ONGOING")

        trip.completed_at = datetime.now()
        self.repository.trip.update(trip, session=session)

    def add_comment(self, trip_id: UUID, driver_id: UUID, rate: int = 0, comment: str = None, session: Session = None):
        trip = self.repository.trip.get_by_id(trip_id, session=session)
        if trip.driver_id != driver_id:
            raise AssertionError(f"TRIP {trip_id} IS NOT DRIVER {driver_id}")
        status = trip_status(trip)
        if status != TripStatus.COMPLETED:
            raise AssertionError(f"TRIP {trip_id} STATUS {status} IS NOT COMPLETED")

        if rate:
            trip.rate_from_driver = rate
        else:
            logging.warn(f"TRIP {trip_id} RATING FROM DRIVER IS NONE")
        if comment:
            trip.comment_from_driver = comment
        else:
            logging.warn(f"TRIP {trip_id} COMMENT FROM DRIVER IS NONE")

        self.repository.trip.update(trip, session=session)

    def get_trip_path(self, orig: LatLon, dest: LatLon) -> List[LatLon]:
        return self.repository.osm.generate_path(orig=orig, dest=dest)