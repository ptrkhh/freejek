import logging
from datetime import datetime
from typing import Literal, List, Union, Optional
from uuid import UUID

from sqlmodel import Session

from backend.entities.trip import Trip
from backend.repository import Repository
from backend.service.util import verify_token_rider
from entities.latlon import LatLon
from entities.trip_status import TripStatus, trip_status, is_trip_active
from entities.web_trip import TripCreationReq, GetTripsResp, GetTripResp, GetDriverResp


class ServiceRiderTrip:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.base_price: int = 5000  # TODO env
        self.distance_price_per_km: int = 5000  # TODO env
        self.vehicle_class_modifier: float = 1.5  # TODO env
        self.vehicle_type_modifier: float = 2.0  # TODO env

    def fare_calculator(self, orig: LatLon, dest: LatLon, vehicle_class: int,
                        vehicle_type: Literal["CAR", "MOTORCYCLE"]) -> int:
        distances = self.repository.osm.calculate_distance_matrix([orig, dest])
        distance_in_m = distances[0][1]
        base_price = self.base_price + int((self.distance_price_per_km * distance_in_m) / 1000)
        vehicle_type_modifier: float = self.vehicle_type_modifier if vehicle_type == "car" else 1.0
        vehicle_class_modifier: float = self.vehicle_class_modifier ** vehicle_class
        # TODO surge pricing
        return int(base_price * vehicle_class_modifier * vehicle_type_modifier)

    def create(self, req: TripCreationReq, session: Session = None) -> UUID:
        assert ((req.passenger < 2 and req.vehicle_type == "MOTORCYCLE") or
                (req.passenger < 9 and req.vehicle_type == "CAR"))

        rider = self.repository.rider.get_by_email(req.email, session=session)
        existing_trips = self.repository.trip.get_by_rider_id(rider.id, session=session)
        if len([i for i in existing_trips if is_trip_active(i)]) > 0:
            raise AssertionError("TRIP ONGOING")

        fair_fare = self.fare_calculator(
            orig=req.pickup,
            dest=req.dropoff,
            vehicle_type=req.vehicle_type,
            vehicle_class=req.vehicle_class,
        )
        if float(abs(req.fare - fair_fare)) / float(fair_fare) > 0.15:
            raise AssertionError("PLEASE RECALCULATE")

        new_trip = self.repository.rider.insert_one(Trip(
            dropoff_lat=req.dropoff.lat,
            dropoff_lon=req.dropoff.lon,
            fare=req.fare,
            passenger=req.passenger,
            pickup_lat=req.pickup.lat,
            pickup_lon=req.pickup.lon,
            request=req.request,
            rider_id=rider.id,
            vehicle_class=req.vehicle_class,
        ), session=session)

        return new_trip.id

    def cancel_trip(self, trip_id: UUID, session: Session = None) -> UUID:
        trip = self.repository.trip.get_by_id(trip_id, session=session)
        if is_trip_active(trip):
            raise
        trip.canceled_at = datetime.now()
        trip = self.repository.trip.update_one(trip, session=session)
        return trip.id

    def change_destination_calculate(self):
        # check how much elapsed, calculate fare as percentage (under 10% or 50m radius, assume 0)
        # find new distance
        # add them, and return only the price
        raise NotImplementedError  # TODO

    def change_destination_commit(self):
        # make sure trip is ongoing, not completed
        # compare fare from request against change_destination_calculate
        # store in database
        raise NotImplementedError  # TODO

    def get_latest_trip(self, token: str, session: Session = None) -> Union[GetTripResp, None]:
        email, phone, is_verified, method = verify_token_rider(token)
        i = self.repository.trip.get_latest_by_rider_email(email=email, session=session)
        if not i:
            return None
        return GetTripResp(
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
            vehicle_make=i.vehicle_make,
            vehicle_model=i.vehicle_model,
            driver_id=i.driver_id,
            rider_id=i.rider_id,
            vehicle_id=i.vehicle_id,
            status=trip_status(i),
        )

    def get_driver(self, driver_id: UUID, session: Session = None) -> GetDriverResp:
        driver = self.repository.driver.get_by_id(driver_id, session=session)
        return GetDriverResp(
            id=driver.id,
            updated_at=driver.updated_at,
            created_at=driver.created_at,
            last_active=driver.last_active,
            last_deactive=driver.last_deactive,
            name=driver.name,
            phone=driver.phone,
            photo_profile=driver.photo_profile,
        )

    def get_trips(self, rider_id: UUID, session: Session = None) -> List[GetTripsResp]:
        trips = self.repository.trip.get_by_rider_id(rider_id, session=session)
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

    def get_trip(self, trip_id: UUID, session: Session = None) -> GetTripResp:
        i = self.repository.trip.get_by_id(trip_id, session=session)
        return GetTripResp(
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
            vehicle_make=i.vehicle_make,
            vehicle_model=i.vehicle_model,
            driver_id=i.driver_id,
            rider_id=i.rider_id,
            vehicle_id=i.vehicle_id,
            status=trip_status(i),
        )

    def add_comment(self, trip_id: UUID, rider_id: UUID, rate: int = 0, comment: str = None, session: Session = None):
        trip = self.repository.trip.get_by_id(trip_id, session=session)
        if trip.rider_id != rider_id:
            raise AssertionError(f"TRIP {trip_id} IS NOT RIDER {rider_id}")
        status = trip_status(trip)
        if status != TripStatus.COMPLETED:
            raise AssertionError(f"TRIP {trip_id} STATUS {status} IS NOT COMPLETED")

        if rate:
            trip.rate_from_rider = rate
        else:
            logging.warn(f"TRIP {trip_id} RATING FROM RIDER IS NONE")
        if comment:
            trip.comment_from_rider = comment
        else:
            logging.warn(f"TRIP {trip_id} COMMENT FROM RIDER IS NONE")

        self.repository.trip.update(trip, session=session)

    def get_trip_path(self, orig: LatLon, dest: LatLon) -> List[LatLon]:
        return self.repository.osm.generate_path(orig=orig, dest=dest)

    def find_poi(self, orig: LatLon, q: Optional[str] = None):
        return self.repository.osm.search_poi(
            orig=orig,
            q=q,
            limit=10 if q else 100,
        )
