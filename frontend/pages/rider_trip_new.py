import traceback

import folium
import streamlit as st
from streamlit import session_state
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from backend.controller.router import Controller
from entities.latlon import LatLon
from entities.trip_status import TripStatus
from frontend.entities.session_state import RiderTripNew
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

c: Controller = st.session_state.controller
t: TokenHandler = st.session_state.token_handler
l: LocationHandler = st.session_state.location_handler
tr: TripHandler = st.session_state.trip_handler

if "rider_trip_new" not in st.session_state:
    st.session_state["rider_trip_new"] = RiderTripNew(
        last_count=0,
        last_clicked=LatLon(lat=0, lon=0),
        search_results=c.rider_search_poi(l.current_location),
        search_query=None,
        last_search_query=None,
        pickup=l.current_location,
        dropoff=l.current_location,
        fare=0,
        fare_pickup=None,
        fare_dropoff=None,
    )
session_state: RiderTripNew = st.session_state["rider_trip_new"]

count = st_autorefresh(interval=5000)  # TODO env var

st.title("Let's go places!")

for i in session_state.search_results:
    st.write(i.name, i.street, i.postal_code)
    if st.button("Set as PICKUP"):
        session_state.pickup = i.location
    if st.button("Set as DROPOFF"):
        session_state.dropoff = i.location


def callback():
    out = st.session_state["folium_map"]["last_clicked"]
    if out and "lat" in out:
        session_state.last_clicked = LatLon(lat=out["lat"], lon=out["lng"])


fg = folium.FeatureGroup(name="Moving Marker")
# TODO fg add child POI
# TODO fg add child last click
# TODO fg add child pickup
# TODO fg add child dropoff (if not same as current location)
# TODO fg add child get path (if dropoff not same as current location)
map_out = st_folium(
    folium.Map(location=[st.session_state["initial_lat"], st.session_state["initial_lon"]], zoom_start=16),
    feature_group_to_add=fg,
    # center=(center_lat, center_lon),
    # width=1200,
    # height=500,
    key="folium_map",
    on_change=callback,
)

if st.button("Set as PICKUP"):
    session_state.pickup = session_state.last_clicked
if st.button("Set as DROPOFF"):
    session_state.dropoff = session_state.last_clicked


# Vehicle Type Selector
vehicle_type = st.radio("Choose your vehicle type:", ["Car", "Bike"])
vehicle_class = st.radio(
    "Choose your vehicle class:",
    ["Economy", "Premium Economy", "Business", "First Class"],
    format_func=lambda x: x
)

vehicle_class_map = {# Economy = Caligra. Premium Economy = Xpanza. Business = Innoxy. First Class = Alphecedes
    "Economy": 0,
    "Premium Economy": 1,
    "Business": 2,
    "First Class": 3
}


selected_vehicle_class = vehicle_class_map[vehicle_class]

passenger_count = st.slider("Passengers:", 1, 6, value=1, disabled=vehicle_type == "Bike")

notes = st.text_area("Notes for the driver:")


session_state.fare = calculate_fare()

# Display calculated fare
st.markdown(f"### Estimated Fare: Rp{session_state.fare:,}")

# Big order button
if st.button("🚗 ORDER RIDE"):
    st.success("Ride Ordered!")
    # You could also trigger backend logic here using trip_handler or other services
    # tr.create_trip(...) etc.



if count != st.session_state.last_count:  # TODO if failure = fine
    last_count = count
    # TODO when (pickup or dstination updated) and (pickup and destination) hit endpoint GET /route/v1/{profile}/{coordinates}?alternatives={true|false}&steps={true|false}&geometries={polyline|polyline6|geojson}&overview={full|simplified|false}&annotations={true|false}

    if count % 3 == 0:
        pass