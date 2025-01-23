from supabase import Client

from backend.repository.example import RepositoryExample
from backend.repository.rider import RepositoryRider
from sqlmodel import select, engine

class Repository:
    def __init__(self, supabase_client: Client, sqlmodel_engine: engine):
        self.supabase_client = supabase_client
        self.sqlmodel_engine = sqlmodel_engine
        self.example = RepositoryExample(supabase_client)
        self.rider = RepositoryRider(sqlmodel_engine)
