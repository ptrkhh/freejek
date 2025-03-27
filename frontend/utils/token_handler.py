import os
from typing import Literal, Optional

from streamlit_local_storage import LocalStorage
import streamlit as st
from data.constant import ACCESS_TOKEN, REFRESH_TOKEN
import jwt
import datetime


class TokenHandler:
    def __init__(self):
        self.ls : LocalStorage = LocalStorage()

    def is_signed_in(self):
        if ACCESS_TOKEN in st.session_state and REFRESH_TOKEN in st.session_state:
            # TODO validate token
            return True
        if self.ls.getItem(ACCESS_TOKEN) and self.ls.getItem(REFRESH_TOKEN):
            # TODO validate token
            self.store_token(ACCESS_TOKEN, REFRESH_TOKEN)
            return True
        # TODO erase access token & refresh token
        return False

    def get_token(self):
        if self.is_signed_in():
            st.session_state[ACCESS_TOKEN] = self.ls.getItem(ACCESS_TOKEN)
            st.session_state[REFRESH_TOKEN] = self.ls.getItem(REFRESH_TOKEN)
            return st.session_state[ACCESS_TOKEN], st.session_state[REFRESH_TOKEN]
        return None, None

    def store_token(self, access_token, refresh_token, status: Optional[Literal["driver", "rider"]] = None):
        if status:
            access_token = self.edit_jwt(access_token, status)
        st.session_state[ACCESS_TOKEN] = access_token
        st.session_state[REFRESH_TOKEN] = refresh_token
        self.ls.setItem(ACCESS_TOKEN, access_token, key=ACCESS_TOKEN)
        self.ls.setItem(REFRESH_TOKEN, refresh_token, key=REFRESH_TOKEN)

    def edit_jwt(self, old_jwt, status: Literal["driver", "rider"]):
        secret_key = os.environ.get("JWT_SECRET")
        algorithm = "HS256"

        decoded_payload = jwt.decode(old_jwt, options={"verify_signature": False})
        decoded_payload["driver_or_rider"] = status
        return jwt.encode(decoded_payload, secret_key, algorithm=algorithm)