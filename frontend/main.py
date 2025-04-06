import os

import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from frontend.utils.init import init

c, t, l, tr = init()
st.title("FREEJEK ALWAYS FREE AF")
st.write("Your Location:", l.current_location.as_tuple())

if 'last_count' not in st.session_state:
    l.update_initial_location()
    st.session_state['last_count'] = 0

fg = folium.FeatureGroup(name="Moving Marker")
if l.initial_location.is_zero():
    st.title("Acquiring your location...")
else:
    out = st_folium(
        folium.Map(location=l.initial_location.as_list(), zoom_start=16),
        feature_group_to_add=fg,
        width=1200,
        height=500,
    )

st.text_input(label="something")

count = st_autorefresh(interval=os.environ.get("PING_DELAY_IDLE", 15) * 1000)

if count != st.session_state.last_count:
    last_count = count
    l.update()
    fg.add_child(folium.CircleMarker(l.current_location.as_list()))

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
