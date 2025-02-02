from sqlmodel import engine
from supabase import Client

from backend.repository.location_history import RepositoryLocationHistory
from backend.repository.osm import RepositoryOsm
from backend.repository.rider import RepositoryRider
from backend.repository.rider import RepositoryRider
from backend.repository.trip import RepositoryTrip
from backend.repository.vehicle_model import RepositoryVehicleModel
from backend.repository.vehicle_unit import RepositoryVehicleUnit


class Repository:
    def __init__(self, postgres: engine, supabase: Client):
        self.postgres = postgres
        self.supabase = supabase
        self.vehicle_model = RepositoryVehicleModel(engine=postgres)
        self.vehicle_unit = RepositoryVehicleUnit(engine=postgres)
        self.rider = RepositoryRider(engine=postgres)
        self.trip = RepositoryTrip(engine=postgres)
        self.location_history = RepositoryLocationHistory(engine=postgres)
        self.osm = RepositoryOsm()
