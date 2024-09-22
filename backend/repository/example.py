from typing import List

from supabase import Client

from backend.entities.example import Example


class RepositoryExample:
    def __init__(self, supabase_client: Client):
        self.client = supabase_client
        self.example_table = self.client.from_("movies")

    def get_examples(self) -> List[Example]:
        return self.example_table.select("*").execute()

    def insert_example(self, example: Example):
        self.example_table.insert(example).execute()
