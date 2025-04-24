from typing import List

import streamlit as st
import traceback

import folium
import streamlit as st
from streamlit import session_state
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from backend.controller.router import Controller
from entities.latlon import LatLon
from entities.trip_status import TripStatus
from entities.web_api import Poi
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

c: Controller = st.session_state.controller
t: TokenHandler = st.session_state.token_handler
l: LocationHandler = st.session_state.location_handler
tr: TripHandler = st.session_state.trip_handler

if not ("pois" in st.session_state and "last_pois_query" in st.session_state):
    st.session_state["pois"]: List[Poi] = c.rider_search_poi(l.current_location)
    st.session_state["last_pois_query"]: str = ""
if "pickup" not in session_state:
    st.session_state["pickup"]: LatLon = l.current_location
if "dropoff" not in session_state:
    st.session_state["dropoff"]: LatLon = l.current_location

st.title("Let's go places!")

pois_query = st.text_input("Where do you want to go today?")
if pois_query != st.session_state["last_pois_query"]:
    st.session_state["pois"] = c.rider_search_poi(l.current_location, pois_query)
    st.session_state["last_pois_query"] = pois_query
pois: List[Poi] = st.session_state["pois"]
for i in pois:
    st.write(i.name, i.street, i.postal_code)
    if st.button("Set as PICKUP"):
        st.session_state["pickup"] = i.location
    if st.button("Set as DROPOFF"):
        st.session_state["dropoff"] = i.location


def callback():
    out = st.session_state["my_map"]["last_clicked"]
    print("THE OUT", out)
    if out and "lat" in out:
        st.session_state["last_clicked_lat"] = out["lat"]
        st.session_state["last_clicked_lon"] = out["lng"]

fg = folium.FeatureGroup(name="Moving Marker")
fg.add_child(update_position())
print("LAST CLICKED", st.session_state["last_clicked_lat"], st.session_state["last_clicked_lon"])
fg.add_child(update_position2(st.session_state["last_clicked_lat"], st.session_state["last_clicked_lon"]))

map_out = st_folium(
    folium.Map(location=[st.session_state["initial_lat"], st.session_state["initial_lon"]], zoom_start=16),
    feature_group_to_add=fg,
    # center=(center_lat, center_lon),
    # width=1200,
    # height=500,
    key="my_map",
    on_change=callback,
)


# TODO show map in center
# TODO tap on map = move dot
# TODO button --> Set as pickup point
# TODO button --> Set as destination
# TODO radio --> vehicle type (car/bike)
# TODO radio --> vehicle class
# TODO slider --> passengers (when bike = disabled)

# TODO when (pickup or dstination updated) and (pickup and destination) hit endpoint GET /route/v1/{profile}/{coordinates}?alternatives={true|false}&steps={true|false}&geometries={polyline|polyline6|geojson}&overview={full|simplified|false}&annotations={true|false}
# TODO and redraw
# TODO and provide fare calculation

# TODO textarea to NOTES FROM RIDER
# TODO ORDER RIDE
