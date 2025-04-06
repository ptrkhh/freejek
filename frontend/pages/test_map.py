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

st.session_state["lat"], st.session_state["lon"] = res["coords"]["latitude"], res["coords"]["longitude"]
# st.session_state["lat"], st.session_state["lon"]=39.949610, -75.150282
st.session_state["initial_lat"], st.session_state["initial_lon"] = st.session_state["lat"], st.session_state["lon"]
last_count = 0
count = st_autorefresh(interval=5000, key="fizzbuzzcounter")


def update_position():
    st.session_state["lat"] = st.session_state["lat"] + random.uniform(-0.001, 0.001)
    st.session_state["lon"] = st.session_state["lon"] + random.uniform(-0.001, 0.001)
    # random_lat = center_lat + random.uniform(-0.001, 0.001)
    # random_lon = center_lon + random.uniform(-0.001, 0.001)
    return folium.RegularPolygonMarker([st.session_state["lat"], st.session_state["lon"]])

def update_position2():
    return folium.CircleMarker([st.session_state["last_clicked"]["lat"], st.session_state["last_clicked"]["lng"]])



fg = folium.FeatureGroup(name="Moving Marker")
fg2 =  folium.FeatureGroup(name="Clicking Marker")
fg.add_child(update_position())
out = st_folium(
    folium.Map(location=[st.session_state["initial_lat"], st.session_state["initial_lon"]], zoom_start=16),
    feature_group_to_add=[fg, fg2],
    # center=(center_lat, center_lon),
    # width=1200,
    # height=500,
)
print("THE OUT", out)

if "last_clicked" in out and out["last_clicked"]:
    st.session_state["last_clicked"] = out["last_clicked"]
    last =  st.session_state["last_clicked"]
    if "lat" in last and last["lat"] and "lng" in last and last["lng"]:
        fg2.add_child(update_position2())

st.text_input(label="something")

if count != last_count:
    last_count = count
    fg.add_child(update_position())
    fg2.add_child(update_position2())
