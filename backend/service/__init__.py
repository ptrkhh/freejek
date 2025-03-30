from backend.repository import Repository
from backend.service.driver_auth import ServiceDriverAuth
from backend.service.master_data import ServiceMasterData
from backend.service.rider_auth import ServiceRiderAuth
from backend.service.rider_trip import ServiceRiderTrip


class Service:
    def __init__(self, repository: Repository):
        self.master_data = ServiceMasterData(repository)
        self.rider_auth = ServiceRiderAuth(repository)
        self.rider_trip = ServiceRiderTrip(repository)
        self.driver_auth = ServiceDriverAuth(repository)
