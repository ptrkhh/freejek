from typing import List
from uuid import UUID

from sqlmodel import Session
from sqlmodel import select, engine

from backend.entities.vehicle_unit import VehicleUnit


class RepositoryVehicleUnit:
    def __init__(self, engine: engine):
        self.engine = engine

    def get_all(self, session: Session = None) -> List[VehicleUnit]:
        sess = session if session else Session(self.engine)
        statement = select(VehicleUnit)
        results: List[VehicleUnit] = sess.execute(statement).scalars().all()
        if session is None:
            sess.close()
        return results

    def get_by_id(self, id: UUID, session: Session = None) -> VehicleUnit:
        sess = session if session else Session(self.engine)
        statement = select(VehicleUnit).where(VehicleUnit.id == id)
        results: VehicleUnit = sess.execute(statement).scalars().one()
        if session is None:
            sess.close()
        return results

    def insert_one(self, item: VehicleUnit, session: Session = None) -> VehicleUnit:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item
