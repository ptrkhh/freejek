from typing import List
from uuid import UUID

from sqlmodel import Session,engine, select

from backend.entities.trip import Trip


class RepositoryTrip:
    def __init__(self, engine: engine):
        self.engine = engine

    def get_by_id(self, id: UUID, session: Session = None) -> Trip:
        sess = session if session else Session(self.engine)
        statement = select(Trip).where(Trip.id == id)
        results: Trip = sess.execute(statement).scalars().one()
        if session is None:
            sess.close()
        return results

    def get_by_driver_id(self, driver_id: UUID, session: Session = None) -> List[Trip]:
        sess = session if session else Session(self.engine)
        statement = select(Trip).where(Trip.driver_id == driver_id)
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
