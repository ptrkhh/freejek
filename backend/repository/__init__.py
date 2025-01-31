from sqlmodel import engine
from supabase import Client

from backend.repository.osm import RepositoryOsm
from backend.repository.rider import RepositoryRider
from backend.repository.rider import RepositoryRider
from backend.repository.trip import RepositoryTrip
from backend.repository.vehicle_model import RepositoryVehicleModel


class Repository:
    def __init__(self, postgres: engine, supabase: Client):
        self.postgres = postgres
        self.supabase = supabase
        self.vehicle_model = RepositoryVehicleModel(engine=postgres)
        self.rider = RepositoryRider(engine=postgres)
        self.trip = RepositoryTrip(engine=postgres)
        self.osm = RepositoryOsm()
