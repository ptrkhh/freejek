from typing import List

from sqlmodel import Session

from backend.entities.vehicle_model import VehicleModel
from entities.web_master_data import WebVehicleModel
from backend.repository import Repository


class ServiceMasterData:
    def __init__(self, repository: Repository):
        self.repository = repository

    def list_all_vehicles(self, session: Session) -> List[WebVehicleModel]:
        all_vehicles: List[VehicleModel] = self.repository.vehicle_model.get_all(session)

        return [WebVehicleModel(
            id=i.id,
            capacity=i.capacity,
            created_at=i.created_at,
            vehicle_class=i.vehicle_class,
            make=i.make,
            model=i.model,
            type=str(i.type),
            propulsion=str(i.propulsion),
        )
            for i in all_vehicles]

