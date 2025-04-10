from datetime import timedelta, datetime, UTC
from typing import List
from uuid import UUID

from sqlalchemy import Engine
from sqlmodel import Session
from sqlmodel import select

from backend.entities.location_history import LocationHistory
from entities.latlon import LatLon


class RepositoryLocationHistory:
    def __init__(self, engine: Engine):
        self.engine = engine

    def insert_one(self, item: LocationHistory, session: Session = None) -> LocationHistory:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item

    def get_by_driver_id(self, driver_id: UUID, timeout: int = 300, session: Session = None) -> List[
        LocationHistory]:  # TODO token
        sess = session if session else Session(self.engine)

        time_limit = datetime.now(tz=UTC) - timedelta(seconds=timeout)
        statement = (
            select(LocationHistory)
            .where(LocationHistory.driver_id == driver_id)
            .where(LocationHistory.created_at > time_limit)
            .order_by(LocationHistory.created_at.asc())
        )
        results: List[LocationHistory] = sess.exec(statement).all()
        if session is None:
            sess.close()
        return results

    def get_by_rider_id(self, rider_id: UUID, timeout: int = 300, session: Session = None) -> List[
        LocationHistory]:  # TODO token
        sess = session if session else Session(self.engine)

        time_limit = datetime.now(tz=UTC) - timedelta(seconds=timeout)
        statement = (
            select(LocationHistory)
            .where(LocationHistory.rider_id == rider_id)
            .where(LocationHistory.created_at > time_limit)
            .order_by(LocationHistory.created_at.asc())
        )
        results: List[LocationHistory] = sess.exec(statement).all()
        if session is None:
            sess.close()
        return results

    def fetch_nearby_drivers(self, locmin: LatLon, locmax: LatLon, timeout: int = 300, session: Session = None) -> List[
        LocationHistory]:  # TODO token
        sess = session if session else Session(self.engine)

        time_limit = datetime.now(tz=UTC) - timedelta(seconds=timeout)
        statement = (
            select(LocationHistory)
            .where(LocationHistory.driver_id is not None)
            .where(LocationHistory.rider_id is None)
            .where(LocationHistory.lat > locmin.lat)
            .where(LocationHistory.lat < locmax.lat)
            .where(LocationHistory.lon > locmin.lon)
            .where(LocationHistory.lon < locmax.lon)
            .where(LocationHistory.created_at > time_limit)
            .order_by(LocationHistory.created_at.desc())
            .group_by(LocationHistory.driver_id)
        )
        results: List[LocationHistory] = sess.exec(statement).all()
        if session is None:
            sess.close()
        return results
