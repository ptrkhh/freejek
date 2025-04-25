import traceback

import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from backend.controller.router import Controller
from entities.latlon import LatLon
from entities.trip_status import TripStatus
from frontend.entities.session_state import RiderTripCurrent
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

c: Controller = st.session_state.controller
t: TokenHandler = st.session_state.token_handler
l: LocationHandler = st.session_state.location_handler
tr: TripHandler = st.session_state.trip_handler

if 'rider_trip_current' not in st.session_state:
    st.session_state["rider_trip_current"] = RiderTripCurrent.zero_value()
session_state: RiderTripCurrent = st.session_state["rider_trip_current"]
count = st_autorefresh(interval=5000)  # TODO env var

fg = folium.FeatureGroup(name="Moving Marker")

if tr.last_trip.status == TripStatus.AVAILABLE:
    st.title("Searching for drivers...")
    st.write("From:", str(tr.last_trip.pickup.as_list()))
    st.write("To:", str(tr.last_trip.dropoff.as_list()))
    st.write("Fare:", str(tr.last_trip.fare))
    st.write("Request:", str(tr.last_trip.request))
    if st.button("Edit Request"):
        # TODO popup screen to change
        pass
    fg.add_child(folium.CircleMarker(l.current_location.as_list()))
    for i in session_state.nearby_drivers:
        fg.add_child(folium.Marker(i.as_list(), color="red"))
    # TODO light blue path for destination


elif tr.last_trip.status == TripStatus.ACCEPTED:
    st.title("We found a driver! Keep your eyes for a...")
    # TODO car picture
    st.write(tr.last_trip.vehicle_color, tr.last_trip.vehicle_make, tr.last_trip.vehicle_model)
    if not session_state.driver_info:
        session_state.driver_info = tr.get_driver()
    if session_state.driver_info:
        # TODO driver image
        st.write(session_state.driver_info.name)
        st.write(session_state.driver_info.phone)  # TODO WA and telegram link (wa.me/62blabla, t.me/+62blablabla)

    st.write("Request:", tr.last_trip.request)
    if st.button("Edit Request"):
        # TODO popup screen to change
        pass

    fg.add_child(folium.CircleMarker(l.current_location.as_list()))
    if session_state.driver_location:
        fg.add_child(folium.CircleMarker(session_state.driver_location.as_list(), color="red"))
    if tr.get_route_path():
        fg.add_child(folium.PolyLine([i.as_tuple() for i in tr.get_route_path()], color="lightblue"))

elif tr.last_trip.status == TripStatus.ONGOING:
    percentage_driven = 123  # TODO time percentage vs. distance percentage, whichever lowest
    st.title(f"You are {percentage_driven}% there!")
    st.write("From:", str(tr.last_trip.pickup.as_list()))
    st.write("To:", str(tr.last_trip.dropoff.as_list()))
    st.write("Fare:", str(tr.last_trip.fare))
    st.write("Request:", tr.last_trip.request)
    if st.button("Edit Request"):
        # TODO popup screen to change
        pass
    fg.add_child(folium.CircleMarker(l.current_location.as_list()))
    if session_state.driver_location:
        fg.add_child(folium.CircleMarker(session_state.driver_location.as_list(), color="red"))
    if tr.get_route_path():
        fg.add_child(folium.PolyLine([i.as_tuple() for i in tr.get_route_path()], color="lightblue"))

elif tr.last_trip.status == TripStatus.COMPLETED:
    st.title("Congratulations! Trip has been completed!")

    st.write("From:", str(tr.last_trip.pickup.as_list()))
    st.write("To:", str(tr.last_trip.dropoff.as_list()))
    st.write("Fare:", str(tr.last_trip.fare))
    driver_star = st.slider("Rate for driver")
    driver_note = st.text_input("Rate for driver")
    if st.button("Rate Driver"):
        tr.rate_driver(
            rider_id=tr.get_last_trip().rider_id,
            trip_id=tr.get_last_trip().trip_id,
            stars=driver_star,
            note=driver_note,
        )
    fg.add_child(folium.CircleMarker(l.current_location.as_list()))


elif tr.last_trip.status == TripStatus.CANCELED:
    st.title("Congratulations! Trip has been completed!")
    #
    # Note from you: <INSERT NOTE>
    # Note from driver: <INSERT NOTE>

out = st_folium(
    folium.Map(location=l.initial_location.as_tuple(), zoom_start=16),
    feature_group_to_add=fg,
    width=1200,
    height=500,
)

if count != session_state.last_count:  # TODO if failure = fine
    session_state.last_count = count
    try:
        l.update(tr.last_trip.id)
    except Exception as e:
        print("ERROR", e)
        traceback.print_exc()

    if tr.last_trip.status in [TripStatus.ACCEPTED, TripStatus.ONGOING]:
        try:
            driver_locations = c.rider_fetch_driver_location(
                driver_id=tr.last_trip.driver_id,
            )
            session_state.driver_location = driver_locations[0]  # TODO trailpath
        except Exception as e:
            print("ERROR", e)
            traceback.print_exc()

    if count % 3 == 0:
        try:
            tr.update()
        except Exception as e:
            print("ERROR", e)
            traceback.print_exc()

        if tr.last_trip.status == TripStatus.AVAILABLE:
            try:
                session_state.nearby_drivers = c.rider_fetch_nearby_drivers(
                    loc=l.current_location,
                    radius=1000,  # TODO increasing if none were found
                    timeout=300,
                )
            except Exception as e:
                print("ERROR", e)
                traceback.print_exc()

st.session_state["rider_trip_current"] = session_state