from supabase import Client

from backend.repository.example import RepositoryExample


class Repository:
    def __init__(self, supabase_client: Client):
        self.example = RepositoryExample(supabase_client)
