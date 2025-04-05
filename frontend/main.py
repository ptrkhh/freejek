import traceback

import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

from backend.controller.router import Controller
from data.latlon import LatLon
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

c = Controller()
st.session_state["controller"] = c
t = TokenHandler()
st.session_state["token_handler"] = t
l = LocationHandler(c, t)
st.session_state["location_handler"] = l
tr = TripHandler(c, t)
st.session_state["trip_handler"] = tr

st.title("FREEJEK ALWAYS FREE AF")

if 'last_count' not in st.session_state:
    l.update_initial_location()
    st.session_state['last_count'] = 0
count = st_autorefresh(interval=2000)  # TODO env var


def update_position():
    st.write("Your Location:", l.current_location.as_tuple())
    return folium.CircleMarker(l.current_location.as_list())


fg = folium.FeatureGroup(name="Moving Marker")
fg.add_child(update_position())
out = st_folium(
    folium.Map(location=l.current_location.as_list(), zoom_start=16),
    feature_group_to_add=fg,
    width=1200,
    height=500,
)

st.text_input(label="something")

if count != st.session_state.last_count:  # TODO if failure = fine
    last_count = count
    try:
        l.update()
    except Exception as e:
        print("ERROR", e)
        traceback.print_exc()
    fg.add_child(update_position())

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
