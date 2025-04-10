from enum import Enum

from backend.entities.trip import Trip


class TripStatus(Enum):
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    ONGOING = "ONGOING"
    ACCEPTED = "ACCEPTED"
    AVAILABLE = "AVAILABLE"


def trip_status(trip: Trip) -> TripStatus:
    if trip.canceled_at:
        return TripStatus.CANCELED
    if trip.completed_at:
        return TripStatus.COMPLETED
    if trip.started_at:
        return TripStatus.ONGOING
    if trip.accepted_at:
        return TripStatus.ACCEPTED
    return TripStatus.AVAILABLE


def is_trip_active(trip: Trip) -> bool:
    status = trip_status(trip)
    if status == TripStatus.CANCELED:
        return False
    if status == TripStatus.COMPLETED:
        return False
    return True


def available_for_driver(trip: Trip) -> bool:
    return TripStatus.PENDING == trip_status(trip)
