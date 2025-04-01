import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium
import folium
from backend.controller.router import Controller
from frontend.utils.token_handler import TokenHandler

st.session_state["controller"] = Controller()
st.session_state["token_handler"] = TokenHandler()

st.title("FREEJEK ALWAYS FREE AF")
print("THE LOCATION", location)
center_lat, center_lon = location["latitude"], location["longitude"]


last_count = 0
count = st_autorefresh(interval=2000, key="fizzbuzzcounter")


def update_position():
    print("THE LOCATION", location)
    center_lat, center_lon = location["latitude"], location["longitude"]
    st.write("Your Location:", center_lat, center_lon)

    return folium.CircleMarker([center_lat, center_lon])


fg = folium.FeatureGroup(name="Moving Marker")
fg.add_child(update_position())
out = st_folium(
    folium.Map(location=[center_lat, center_lon], zoom_start=16),
    feature_group_to_add=fg,
    center=(center_lat, center_lon),
    width=1200,
    height=500,
)

st.text_input(label="something")

if count != last_count:
    last_count = count
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
