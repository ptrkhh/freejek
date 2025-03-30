import streamlit as st

from backend.controller.router import Controller
from frontend.utils.token_handler import TokenHandler

st.session_state["controller"] = Controller()
st.session_state["token_handler"] = TokenHandler()

st.title("FREEJEK ALWAYS FREE AF")

# TODO ask GPS permission. NO GPS = NO USE
# TODO sidebar
# if token not exist: rider signin, driver signin
# if token rider:
#     if token rider & ride in progress - show current ride
#     if token rider & ride not in progress - show new ride
#     show ride history, rider settings
#     show logout
# if token driver:
#     if token driver & ride in progress - show current ride
#     if token driver & rider not in progress - show search ride
#     show ride history, driver settings
#     show logout
