import os
import traceback
from typing import Literal

import jwt
from streamlit_local_storage import LocalStorage

from data.constant import ACCESS_TOKEN, REFRESH_TOKEN


class TokenHandler:
    def __init__(self):
        self.ls: LocalStorage = LocalStorage()
        self.secret_key: str = os.environ.get("JWT_SECRET")

    def is_signed_in(self):
        try:
            if self.ls.getItem(ACCESS_TOKEN) and self.ls.getItem(REFRESH_TOKEN):
                # TODO validate token
                return True
        # TODO erase access token & refresh token
        except Exception as e:
            print("ERROR WHEN RETRIEVING TOKEN", e)
            traceback.print_exc()
        self.clear_token()
        return False

    def get_token(self):
        if self.is_signed_in():
            return self.ls.getItem(ACCESS_TOKEN)
        self.clear_token()
        return None

    def get_refresh_token(self):
        if self.is_signed_in():
            return self.ls.getItem(REFRESH_TOKEN)
        self.clear_token()
        return None

    def get_email(self):
        access_token, refresh_token = self.get_token()
        if not access_token:
            self.clear_token()
            return None
        payload = jwt.decode(access_token, self.secret_key, audience="authenticated", algorithms=["HS256"])
        return payload.get("email")

    def is_driver(self):
        access_token, refresh_token = self.get_token()
        if not access_token:
            self.clear_token()
            return False
        payload = jwt.decode(access_token, self.secret_key, audience="authenticated", algorithms=["HS256"])
        return payload.get("driver_or_rider") == "driver"

    def is_rider(self):
        access_token, refresh_token = self.get_token()
        if not access_token:
            self.clear_token()
            return False
        payload = jwt.decode(access_token, self.secret_key, audience="authenticated", algorithms=["HS256"])
        return payload.get("driver_or_rider") == "rider"

    def store_token(self, access_token: str, refresh_token: str, status: Literal["driver", "rider"]):
        access_token = self._edit_jwt(access_token, status)
        self.ls.setItem(ACCESS_TOKEN, access_token, key=ACCESS_TOKEN)
        self.ls.setItem(REFRESH_TOKEN, refresh_token, key=REFRESH_TOKEN)

    def _edit_jwt(self, old_jwt: str, status: Literal["driver", "rider"]):
        secret_key = os.environ.get("JWT_SECRET")
        print("THE SECRET KEY", secret_key)
        algorithm = "HS256"

        decoded_payload = jwt.decode(old_jwt, secret_key, audience="authenticated", algorithms=["HS256"])
        decoded_payload["driver_or_rider"] = status
        return jwt.encode(decoded_payload, secret_key, algorithm=algorithm)

    def clear_token(self):
        self.ls.setItem(ACCESS_TOKEN, None)
        self.ls.setItem(REFRESH_TOKEN, None)
