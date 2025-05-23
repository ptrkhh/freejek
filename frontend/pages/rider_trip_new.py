import traceback

import folium
import streamlit as st
from streamlit import session_state
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from backend.controller.router import Controller
from entities.constant import VEHICLE_CLASS_INDEX
from entities.latlon import LatLon
from entities.web_trip import FareCalculatorReq, TripCreationReq
from frontend.entities.session_state import RiderTripNew
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

c: Controller = st.session_state.controller
t: TokenHandler = st.session_state.token_handler
l: LocationHandler = st.session_state.location_handler
tr: TripHandler = st.session_state.trip_handler

if "rider_trip_new" not in st.session_state:
    st.session_state["rider_trip_new"] = RiderTripNew.zero_value(l.current_location)
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
for i in session_state.search_results:
    fg.add_child(folium.CircleMarker(l.current_location.as_tuple()))
fg.add_child(folium.CircleMarker(session_state.last_clicked.as_tuple()))
fg.add_child(folium.CircleMarker(session_state.pickup.as_tuple()))
if session_state.pickup != session_state.dropoff:
    fg.add_child(folium.CircleMarker(session_state.dropoff.as_tuple()))
    if session_state.path:
        fg.add_child(folium.PolyLine([i.as_tuple() for i in session_state.path]))
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
vehicle_type: str = st.radio("Choose your vehicle type:", ["Car", "Motorcycle"])
vehicle_class: int = st.radio(
    "Choose your vehicle class:",
    range(len(VEHICLE_CLASS_INDEX)),
    format_func=lambda x: VEHICLE_CLASS_INDEX[x],
)

passenger_count = st.slider("Passengers:", 1, 6, value=1, disabled=vehicle_type == "Bike")

notes = st.text_area("Notes for the driver:")

req = session_state.fare_req
updated_pickup = session_state.pickup != req.orig if req else True
updated_dropoff = session_state.dropoff != req.dest if req else True
updated_vehicle_class = vehicle_class != req.vehicle_class if req else True
updated_vehicle_type = vehicle_type.lower() != req.vehicle_type.lower() if req else True
fare_is_calculated_well = session_state.fare and (not (updated_pickup or updated_dropoff or updated_vehicle_class or updated_vehicle_type))
if fare_is_calculated_well:
    st.markdown(f"### Estimated Fare: Rp{session_state.fare:,}")
else:
    st.markdown(f"### Estimated Fare: Calculating...")

# Big order button
if st.button("🚗 ORDER RIDE", disabled=not fare_is_calculated_well):
    try:
        c.rider_trip_create(req=TripCreationReq(
            email=t.get_email(),
            pickup=session_state.pickup,
            dropoff=session_state.dropoff,
            vehicle_class=session_state.vehicle_class,
            vehicle_type="CAR" if vehicle_type.lower() == "car" else "MOTORCYCLE",
            request=notes,
            passenger=passenger_count,
            fare=session_state.fare,
        ))
        st.success("Ride Ordered!")
        time.sleep(2)
        st.switch_page("pages/rider_trip_current.py")
    except Exception as e:
        # TODO report with ID
        print(e)
        print(traceback.format_exc())
        st.error("Something went wrong!")

if count != st.session_state.last_count:  # TODO if failure = fine
    last_count = count
    if updated_vehicle_type or updated_vehicle_class or updated_dropoff or updated_pickup:
        try:
            req = FareCalculatorReq(
                orig=session_state.pickup,
                dest=session_state.dropoff,
                vehicle_class=vehicle_class,
                vehicle_type="CAR" if vehicle_type.lower() == "car" else "MOTORCYCLE",
            )
            session_state.fare = c.fare_calculator(req)
            session_state.fare_req = req
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            st.error("Something went wrong when calculating fare!")

    if updated_pickup or updated_dropoff:
        try:
            session_state.path = c.rider_get_trip_path(session_state.pickup, session_state.dropoff)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            st.error("Something went wrong when getting path!")
    if count % 3 == 0:
        pass

st.session_state["rider_trip_new"] = session_state
