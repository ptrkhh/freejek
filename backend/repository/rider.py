from sqlmodel import Session
from sqlmodel import select, engine

from backend.entities.rider import Rider


class RepositoryRider:
    def __init__(self, engine: engine):
        self.engine = engine

    def get_by_id(self, email: str, session: Session = None) -> Rider:
        sess = session if session else Session(self.engine)
        statement = select(Rider).where(Rider.email == email)
        results: Rider = sess.execute(statement).scalars().one()
        if session is None:
            sess.close()
        return results

    def insert_one(self, item: Rider, session: Session = None) -> Rider:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item

    def update_one(self, item: Rider, session: Session = None) -> Rider:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item
