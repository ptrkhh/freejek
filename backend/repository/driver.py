from uuid import UUID

from sqlalchemy import Engine
from sqlmodel import Session
from sqlmodel import select

from backend.entities.driver import Driver


class RepositoryDriver:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.cache = {} # TODO

    def get_by_email(self, email: str, session: Session = None) -> Driver:
        sess = session if session else Session(self.engine)
        statement = select(Driver).where(Driver.email == email)
        results: Driver = sess.exec(statement).one()
        if session is None:
            sess.close()
        return results

    def get_by_auth_id(self, auth_id: UUID, session: Session = None) -> Driver:
        sess = session if session else Session(self.engine)
        statement = select(Driver).where(Driver.auth_id == auth_id)
        results: Driver = sess.exec(statement).one()
        if session is None:
            sess.close()
        return results

    def get_by_id(self, id: UUID, session: Session = None) -> Driver:
        sess = session if session else Session(self.engine)
        statement = select(Driver).where(Driver.id == id)
        results: Driver = sess.exec(statement).one()
        if session is None:
            sess.close()
        return results

    def insert_one(self, item: Driver, session: Session = None) -> Driver:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item

    def update_one(self, item: Driver, session: Session = None) -> Driver:
        sess = session if session else Session(self.engine)
        sess.add(item)
        sess.commit()
        sess.refresh(item)
        if session is None:
            sess.close()
        return item
