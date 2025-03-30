from typing import List

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from backend.controller.router import Controller
from data.latlon import LatLon
from data.trip_status import TripStatus
from entities.web_trip import GetTripResp
from frontend.utils.token_handler import TokenHandler

c: Controller = st.session_state.controller
t: TokenHandler = st.session_state.token_handler

if 'last_trip' not in st.session_state:
    st.session_state["last_trip"] = c.rider_get_latest_trip(t.get_token())
if 'last_count' not in st.session_state:
    st.session_state['last_count'] = 0
if 'my_location' not in st.session_state:
    st.session_state['my_location']: LatLon = LatLon(lat=0.0, lon=0.0)  # TODO trailpath
if 'driver_location' not in st.session_state:
    st.session_state['driver_location']: LatLon = LatLon(lat=0.0, lon=0.0)  # TODO trailpath
if 'nearby_drivers' not in st.session_state:
    st.session_state['nearby_drivers']: List[LatLon] = []

count = st_autorefresh(interval=5000)
last_trip: GetTripResp = st.session_state.last_trip

if count != st.session_state.last_count:  # TODO if failure = fine
    last_count = count
    # TODO update my location
    # TODO ping my location to cloud

    if last_trip.status in [TripStatus.ACCEPTED, TripStatus.ONGOING]:
        pass
        # TODO update driver location

    if count % 3 == 0:
        pass
        # TODO update last trip
        if last_trip.status == TripStatus.AVAILABLE:
            pass
            # TODO update nearby drivers

if last_trip.status == TripStatus.AVAILABLE:
    pass
    # Searching for drivers...
    #
    # From: <ADDRESS>
    # To: <ADDRESS>
    # Fare: <INSERT FARE>
    # Note: <SOME TEXT>
    # (button: Edit Request)
    #
    # Map: Blue dot for you, light blue path, red ring for other drivers


elif last_trip.status == TripStatus.ACCEPTED:
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

elif last_trip.status == TripStatus.ONGOING:
    pass
    # You are xx % there! (time percentage vs. distance percentage, whichever lowest)
    #
    # Note: <SOME TEXT>
    # Your Note: <SOME TEXT>
    # (button: Edit Request)
    #
    # Map: Blue dot for you, light blue path, red dot for the driver

elif last_trip.status == TripStatus.COMPLETED:
    pass
    # Congratulations! Trip has been completed!
    #
    # From: <ADDRESS>
    # To: <ADDRESS>
    # Fare: <INSERT FARE>
    # Map: Blue dot for you

elif last_trip.status == TripStatus.CANCELED:
    pass
    # Trip has been canceled! :(
    #
    # Note from you: <INSERT NOTE>
    # Note from driver: <INSERT NOTE>
