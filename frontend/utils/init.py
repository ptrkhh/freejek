from typing import Tuple

import streamlit as st

from backend.controller.router import Controller
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

def init() -> Tuple[Controller, TokenHandler, LocationHandler, TripHandler]:
    if "controller" not in st.session_state:
        st.session_state["controller"] = Controller()
    c = st.session_state["controller"]
    if "token_handler" not in st.session_state:
        st.session_state["token_handler"] = TokenHandler(c)
    t = st.session_state["token_handler"]
    # TODO show popup asking for GPS permission. Never give up because NO GPS = THIS APP IS NO USE
    if "location_handler" not in st.session_state:
        st.session_state["location_handler"] = LocationHandler(c, t)
    l = st.session_state["location_handler"]
    if "trip_handler" not in st.session_state:
        st.session_state["trip_handler"] = TripHandler(c, t)
    tr = st.session_state["trip_handler"]
    return c, t, l, tr
