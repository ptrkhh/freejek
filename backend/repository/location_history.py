from sqlmodel import Session, engine

from backend.entities.location_history import LocationHistory


class RepositoryLocationHistory:
    def __init__(self, engine: engine):
        self.engine = engine

    def insert_one(self, item: LocationHistory, session: Session = None) -> LocationHistory:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item
