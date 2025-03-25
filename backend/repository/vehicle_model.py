from typing import List
from uuid import UUID

from sqlalchemy.engine import Engine
from sqlmodel import Session
from sqlmodel import select

from backend.entities.vehicle_model import VehicleModel


class RepositoryVehicleModel:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_all(self, session: Session = None) -> List[VehicleModel]:
        sess = session if session else Session(self.engine)
        statement = select(VehicleModel)
        results: List[VehicleModel] = sess.execute(statement).scalars().all()
        if session is None:
            sess.close()
        return results

    def get_by_id(self, id: UUID, session: Session = None) -> VehicleModel:
        sess = session if session else Session(self.engine)
        statement = select(VehicleModel).where(VehicleModel.id == id)
        results: VehicleModel = sess.execute(statement).scalars().one()
        if session is None:
            sess.close()
        return results

    def insert_one(self, item: VehicleModel, session: Session = None) -> VehicleModel:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item
