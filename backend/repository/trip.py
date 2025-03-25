from typing import List, Union
from uuid import UUID

from sqlalchemy.engine import Engine
from sqlmodel import Session, select, and_
from sqlmodel.sql.expression import SelectOfScalar

from backend.entities.latlon import LatLon
from backend.entities.trip import Trip, TripStatus


class RepositoryTrip:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_by_pickup_region(self, minlatlon: LatLon, maxlatlon: LatLon, session: Session = None) -> List[Trip]:
        sess = session if session else Session(self.engine)

        minlatlon.lat, maxlatlon.lat = min(minlatlon.lat, maxlatlon.lat), max(minlatlon.lat, maxlatlon.lat)
        minlatlon.lon, maxlatlon.lon = min(minlatlon.lon, maxlatlon.lon), max(minlatlon.lon, maxlatlon.lon)
        statement = select(Trip).where(and_(
            Trip.pickup_lat >= minlatlon.lat,
            Trip.pickup_lat <= maxlatlon.lat,
            Trip.pickup_lon >= minlatlon.lon,
            Trip.pickup_lon <= maxlatlon.lon,
        ))  # TODO page and limit
        statement = self._filter_by_status(TripStatus.AVAILABLE, statement)
        results: List[Trip] = sess.execute(statement).scalars().all()
        if session is None:
            sess.close()
        return results

    def get_by_id(self, id: UUID, session: Session = None) -> Trip:
        sess = session if session else Session(self.engine)
        statement = select(Trip).where(Trip.id == id)
        results: Trip = sess.execute(statement).scalars().one()
        if session is None:
            sess.close()
        return results

    def get_by_driver_id(self,
                         driver_id: UUID,
                         status: Union[TripStatus, None] = None,
                         session: Session = None,
                         ) -> List[Trip]:
        sess = session if session else Session(self.engine)
        statement = select(Trip).where(Trip.driver_id == driver_id)
        statement = self._filter_by_status(status, statement)
        results: List[Trip] = sess.execute(statement).scalars().all()
        if session is None:
            sess.close()
        return results

    def get_by_rider_id(self, rider_id: UUID, session: Session = None) -> List[Trip]:
        sess = session if session else Session(self.engine)
        statement = select(Trip).where(Trip.rider_id == rider_id)
        results: List[Trip] = sess.execute(statement).scalars().all()
        if session is None:
            sess.close()
        return results

    def insert_one(self, item: Trip, session: Session = None) -> Trip:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item

    def update_one(self, item: Trip, session: Session = None) -> Trip:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item

    def _filter_by_status(self, status: Union[TripStatus, None], statement: SelectOfScalar[Trip]) -> SelectOfScalar[
        Trip]:
        if status is None:
            return statement
        if status == TripStatus.AVAILABLE:
            return statement.where(and_(
                Trip.started_at == None,
                Trip.canceled_at == None,
                Trip.accepted_at == None,
                Trip.completed_at == None,
            ))
        if status == TripStatus.ACCEPTED:
            raise NotImplementedError("STATUS NOT IMPLEMENTED")  # TODO
        if status == TripStatus.CANCELED:
            raise NotImplementedError("STATUS NOT IMPLEMENTED")
        if status == TripStatus.COMPLETED:
            raise NotImplementedError("STATUS NOT IMPLEMENTED")
        if status == TripStatus.ONGOING:
            raise NotImplementedError("STATUS NOT IMPLEMENTED")
        raise AssertionError("STATUS NOT SUPPORTED")
