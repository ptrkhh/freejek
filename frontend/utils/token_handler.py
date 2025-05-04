import os
import traceback
from typing import Literal, Dict, Optional

import jwt
from jwt import ExpiredSignatureError
from streamlit_local_storage import LocalStorage

from backend.controller.router import Controller
from entities.constant import ACCESS_TOKEN, REFRESH_TOKEN


class TokenHandler:
    def __init__(self, c: Controller):
        self.c: Controller = c
        self.ls: LocalStorage = LocalStorage()
        self.secret_key: str = os.environ.get("JWT_SECRET")
        self.algorithm: str = "HS256"

    def is_signed_in(self):
        try:
            self.validate_token(self.get_token(), self.get_refresh_token())
            return True
        except FileNotFoundError:
            return False
        except ExpiredSignatureError:
            return False
        except Exception as e:
            print("ERROR WHEN RETRIEVING TOKEN", e)
            traceback.print_exc()
        self.clear_token()
        return False

    def validate_token(self, access_token: str = None, refresh_token: str = None):  # TODO move to backend
        if not (access_token and refresh_token):
            access_token, refresh_token = self.get_token(), self.get_refresh_token()
        if not (access_token and refresh_token):
            raise FileNotFoundError("TOKEN NOT FOUND")
        try:
            jwt.decode(access_token, self.secret_key, audience="authenticated", algorithms=[self.algorithm])
        except ExpiredSignatureError:  # refresh
            payload = self._decode(access_token, options={'verify_exp': False})
            try:
                access_token, refresh_token = self.c.rider_refresh_token(refresh_token)
                self.store_token(access_token, refresh_token, payload.get("driver_or_rider"))
            except ExpiredSignatureError:  # refresh
                self.clear_token()
            except Exception as e:
                self.clear_token()
                print("ERROR WHEN REFRESHING TOKEN", e)
                traceback.print_exc()

    def get_token(self):
        return self.ls.getItem(ACCESS_TOKEN)

    def get_refresh_token(self):
        return self.ls.getItem(REFRESH_TOKEN)

    def get_email(self):
        access_token = self.get_token()
        if not access_token:
            self.clear_token()
            return None
        payload = self._decode(access_token)
        return payload.get("email")

    def is_driver(self):
        access_token = self.get_token()
        if not access_token:
            self.clear_token()
            return False
        payload = self._decode(access_token)
        return payload.get("driver_or_rider") == "driver"

    def is_rider(self):
        access_token = self.get_token()
        if not access_token:
            self.clear_token()
            return False
        payload = self._decode(access_token)
        return payload.get("driver_or_rider") == "rider"

    def store_token(self, access_token: str, refresh_token: str, status: Literal["driver", "rider"]):
        access_token = self._edit_jwt(access_token, status)
        self.ls.setItem(ACCESS_TOKEN, access_token, key=ACCESS_TOKEN)
        self.ls.setItem(REFRESH_TOKEN, refresh_token, key=REFRESH_TOKEN)

    def _edit_jwt(self, access_token: str, status: Literal["driver", "rider"]):  # TODO move to backend
        payload = self._decode(access_token)
        payload["driver_or_rider"] = status
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def _decode(self, access_token: str, options: Optional[Dict] = None): # TODO remove
        return jwt.decode(
            jwt=access_token,
            key=self.secret_key,
            audience="authenticated",
            algorithms=[self.algorithm],
            options=options,
        )

    def clear_token(self):
        self.ls.deleteItem(ACCESS_TOKEN, key=ACCESS_TOKEN)
        self.ls.deleteItem(REFRESH_TOKEN, key=REFRESH_TOKEN)
