import random
import time

import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

res = get_geolocation()
while not res:
    time.sleep(1)

if not ("lat" in st.session_state and "lon" in st.session_state):
    st.session_state["lat"], st.session_state["lon"] = res["coords"]["latitude"], res["coords"]["longitude"]
if not ("initial_lat" in st.session_state and "initial_lon" in st.session_state):
    st.session_state["initial_lat"], st.session_state["initial_lon"] = st.session_state["lat"], st.session_state["lon"]
if not ("last_clicked_lat" in st.session_state and "last_clicked_lon" in st.session_state):
    st.session_state["last_clicked_lat"], st.session_state["last_clicked_lon"] = 0.0, 0.0
if "last_count" not in st.session_state:
    st.session_state["last_count"] = 0
count = st_autorefresh(interval=5000, key="fizzbuzzcounter")


def update_position():
    st.session_state["lat"] = st.session_state["lat"] + random.uniform(-0.001, 0.001)
    st.session_state["lon"] = st.session_state["lon"] + random.uniform(-0.001, 0.001)
    return folium.RegularPolygonMarker([st.session_state["lat"], st.session_state["lon"]])

def update_position2(lat, lon):
    print("ADDING CIRCLE MARKER AT", lat, lon)
    return folium.CircleMarker([lat, lon])

def callback():
    out = st.session_state["my_map"]["last_clicked"]
    print("THE OUT", out)
    if out and "lat" in out:
        st.session_state["last_clicked_lat"] = out["lat"]
        st.session_state["last_clicked_lon"] = out["lng"]
    # fg.add_child(update_position2(st.session_state["last_clicked_lat"], st.session_state["last_clicked_lon"]))

fg = folium.FeatureGroup(name="Moving Marker")
fg.add_child(update_position())
print("LAST CLICKED", st.session_state["last_clicked_lat"], st.session_state["last_clicked_lon"])
fg.add_child(update_position2(st.session_state["last_clicked_lat"], st.session_state["last_clicked_lon"]))
out = st_folium(
    folium.Map(location=[st.session_state["initial_lat"], st.session_state["initial_lon"]], zoom_start=16),
    feature_group_to_add=fg,
    # center=(center_lat, center_lon),
    # width=1200,
    # height=500,
    key="my_map",
    on_change=callback,
)
#
# if "last_clicked" in out and out["last_clicked"]:
#     print('THE LAST CLICKED1', out["last_clicked"])
#     st.session_state["last_clicked_lat"] = out["last_clicked"]["lat"]
#     st.session_state["last_clicked_lon"] = out["last_clicked"]["lng"]

st.text_input(label="something")

if count != st.session_state["last_count"]:
    last_count = count

