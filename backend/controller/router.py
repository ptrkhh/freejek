import logging
import os
from typing import List, Union, Optional
from uuid import UUID

from
from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlmodel import create_engine, Session
from supabase import create_client, Client

from backend.repository import Repository
from backend.service import Service
from entities.latlon import LatLon
from entities.web_master_data import WebVehicleModel
from entities.web_trip import GetTripResp, GetDriverResp


class Controller:
    def __init__(self):
        load_dotenv()
        self.postgres: Engine = create_engine(os.environ.get("POSTGRES_URL"))
        self.supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
        self.service = Service(Repository(self.postgres, self.supabase))
        self.logger = logging.getLogger(__name__)

    def all_vehicles(self):
        with Session(self.postgres) as session:
            res: List[WebVehicleModel] = self.service.master_data.list_all_vehicles(
                session=session,
            )
        return res

    def driver_get_trip_path(self, orig: LatLon, dest: LatLon):
        return self.service.driver_trip.get_trip_path(orig, dest)

    def rider_sign_up(self, email: str):
        with Session(self.postgres) as session:
            res = self.service.rider_auth.rider_email_sign_up(
                email=email,
                session=session,
            )
            session.commit()
        return res

    # def rider_sign_in(self, email: str, password: str):
    #     with Session(self.postgres) as session:
    #         res = self.service.rider_auth.rider_email_sign_in(
    #             email=email,
    #             password=password,
    #             session=session,
    #         )
    #         session.commit()
    #     return res

    def rider_otp_request(self, email: str):
        with Session(self.postgres) as session:
            res = self.service.rider_auth.rider_email_otp_request(
                email=email,
                session=session,
            )
            session.commit()
        return res

    def rider_otp_verify(self, email: str, otp: str, password: str) -> (str, str):
        with Session(self.postgres) as session:
            access_token, refresh_token = self.service.rider_auth.rider_email_otp_verify(
                email=email,
                otp=otp,
                password=password,
                session=session,
            )
            session.commit()
        return access_token, refresh_token

    def rider_refresh_token(self, refresh_token: str) -> (str, str):
        return self.service.rider_auth.refresh_token(refresh_token)

    def rider_get_latest_trip(self, token: str) -> Union[GetTripResp, None]:
        with Session(self.postgres) as session:
            res = self.service.rider_trip.get_latest_trip(
                token=token,
                session=session,
            )
        return res

    def rider_get_driver(self, driver_id: UUID) -> Union[GetDriverResp, None]:
        with Session(self.postgres) as session:
            res = self.service.rider_trip.get_driver(
                driver_id=driver_id,
                session=session,
            )
        return res

    def rider_ping_location(self, loc: LatLon, email: str, trip_id: UUID = None):
        with Session(self.postgres) as session:
            self.service.ping_location.ping_rider_location(loc, email, trip_id, session)
            session.commit()
        return

    def rider_fetch_driver_location(self, driver_id: UUID, timeout: int = 300) -> List[LatLon]:
        with Session(self.postgres) as session:
            res = self.service.ping_location.fetch_driver_location(
                driver_id=driver_id,
                timeout=timeout,
                session=session,
            )
        return res

    def rider_fetch_nearby_drivers(self, loc: LatLon, radius: int = 1000, timeout: int = 300) -> List[LatLon]:
        with Session(self.postgres) as session:
            res = self.service.ping_location.fetch_nearby_drivers(
                loc=loc,
                radius=radius,
                timeout=timeout,
                session=session,
            )
        return res

    def rider_get_trip_path(self, orig: LatLon, dest: LatLon):
        return self.service.rider_trip.get_trip_path(orig, dest)

    def rider_search_poi(self, orig: LatLon, q: Optional[str] = None):
        return self.service.rider_trip.find_poi(orig, q)

    def rider_rate_driver(self, rider_id: UUID, trip_id: UUID, stars: int, note: str):
        with Session(self.postgres) as session:
            res = self.service.rider_trip.add_comment(
                rider_id=rider_id,
                trip_id=trip_id,
                rate=stars,
                comment=note,
            )
            session.commit()
        return res
