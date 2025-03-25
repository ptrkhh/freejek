from sqlalchemy.engine import Engine
from sqlmodel import Session

from backend.entities.location_history import LocationHistory


class RepositoryLocationHistory:
    def __init__(self, engine: Engine):
        self.engine = engine

    def insert_one(self, item: LocationHistory, session: Session = None) -> LocationHistory:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item
