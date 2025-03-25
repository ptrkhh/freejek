import logging
import os
from typing import List

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlmodel import create_engine, Session
from supabase import create_client, Client

from backend.entities.web_master_data import WebVehicleModel
from backend.repository import Repository
from backend.service import Service

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self):
        load_dotenv()
        self.postgres: Engine = create_engine(os.environ.get("POSTGRES_URL"))
        self.supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
        self.service = Service(Repository(self.postgres, self.supabase))
        self.logger = logging.getLogger(__name__)

    def all_vehicles(self):
        with Session(self.postgres) as session:
            res: List[WebVehicleModel] = self.service.master_data.list_all_vehicles(session=session)
            session.commit()
        return res

    def rider_list_all_vehicles(self, token: str):
        with Session(self.postgres) as session:
            res = self.service.master_data.rider_list_all_vehicles(session=session, token=token)
        return res

    def rider_sign_up(self, email: str):
        with Session(self.postgres) as session:
            print("THE SESSION", session)
            print("THE SERVICE", self.service)
            print("THE RIDER AUTH", self.service.rider_auth)
            res = self.service.rider_auth.rider_email_sign_up(email, session=session)
            session.commit()
        return res

    def rider_sign_in(self, email: str, password: str):
        with Session(self.postgres) as session:
            print("THE SESSION", session)
            print("THE SERVICE", self.service)
            print("THE RIDER AUTH", self.service.rider_auth)
            res = self.service.rider_auth.rider_email_sign_in(email, password, session=session)
            session.commit()
        return res

    def rider_otp_request(self, email: str):
        with Session(self.postgres) as session:
            print("THE SESSION", session)
            print("THE SERVICE", self.service)
            print("THE RIDER AUTH", self.service.rider_auth)
            res = self.service.rider_auth.rider_otp_request(email, session=session)
            session.commit()
        return res

    def rider_otp_verify(self, email: str, otp: str, password: str):
        with Session(self.postgres) as session:
            print("THE SESSION", session)
            print("THE SERVICE", self.service)
            print("THE RIDER AUTH", self.service.rider_auth)
            access_token, refresh_token = self.service.rider_auth.rider_email_otp_verify(email, otp, password, session=session)
            session.commit()
        return access_token, refresh_token
