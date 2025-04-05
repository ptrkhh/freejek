import traceback
from typing import List

import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from backend.controller.router import Controller
from data.latlon import LatLon
from data.trip_status import TripStatus
from frontend.utils.location_handler import LocationHandler
from frontend.utils.token_handler import TokenHandler
from frontend.utils.trip_handler import TripHandler

c: Controller = st.session_state.controller
t: TokenHandler = st.session_state.token_handler
l: LocationHandler = st.session_state.location_handler
tr: TripHandler = st.session_state.trip_handler

if 'last_count' not in st.session_state:
    st.session_state['last_count'] = 0
    l.update_initial_location()
if 'driver_location' not in st.session_state:
    st.session_state['driver_location']: LatLon = LatLon(lat=0.0, lon=0.0)  # TODO trailpath
if 'nearby_drivers' not in st.session_state:
    st.session_state['nearby_drivers']: List[LatLon] = []

count = st_autorefresh(interval=5000)  # TODO env var

fg = folium.FeatureGroup(name="Moving Marker")
out = st_folium(
    folium.Map(location=l.initial_location.as_list(), zoom_start=16),
    feature_group_to_add=fg,
    width=1200,
    height=500,
)

if tr.last_trip.status == TripStatus.AVAILABLE:
    st.title("Searching for drivers...")

    fg.add_child(folium.CircleMarker(l.current_location.as_list()))
    for i in st.session_state["nearby_drivers"]:
        fg.add_child(folium.Marker(i.as_list()))

    # Searching for drivers...
    #
    # From: <ADDRESS>
    # To: <ADDRESS>
    # Fare: <INSERT FARE>
    # Note: <SOME TEXT>
    # (button: Edit Request)
    #
    # Map: Blue dot for you, light blue path, red ring for other drivers


elif tr.last_trip.status == TripStatus.ACCEPTED:
    pass
    # Watch out for...
    # <car picture>
    # Car: <color> <type>
    # Phone: <phone> <WA link> <telegram link>
    # Note:
    #
    #
    # Your Note: <SOME TEXT>
    # (button: Edit Request)
    #
    # Map: Blue dot for you, light blue path, red dot for the driver

elif tr.last_trip.status == TripStatus.ONGOING:
    pass
    # You are xx % there! (time percentage vs. distance percentage, whichever lowest)
    #
    # Note: <SOME TEXT>
    # Your Note: <SOME TEXT>
    # (button: Edit Request)
    #
    # Map: Blue dot for you, light blue path, red dot for the driver

elif tr.last_trip.status == TripStatus.COMPLETED:
    pass
    # Congratulations! Trip has been completed!
    #
    # From: <ADDRESS>
    # To: <ADDRESS>
    # Fare: <INSERT FARE>
    # Map: Blue dot for you

elif tr.last_trip.status == TripStatus.CANCELED:
    pass
    # Trip has been canceled! :(
    #
    # Note from you: <INSERT NOTE>
    # Note from driver: <INSERT NOTE>

if count != st.session_state.last_count:  # TODO if failure = fine
    last_count = count
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
            st.session_state["driver_location"] = driver_locations[0]  # TODO trailpath
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
                st.session_state['nearby_drivers'] = c.rider_fetch_nearby_drivers(
                    loc=l.current_location,
                    radius=1000,  # TODO increasing if none were found
                    timeout=300,
                )
            except Exception as e:
                print("ERROR", e)
                traceback.print_exc()
