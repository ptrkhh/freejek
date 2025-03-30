import streamlit as st
import folium
import random
import time

from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

center_lat, center_lon = 39.949610, -75.150282
last_count = 0
count = st_autorefresh(interval=2000, key="fizzbuzzcounter")

def update_position():
    random_lat = center_lat + random.uniform(-0.001, 0.001)
    random_lon = center_lon + random.uniform(-0.001, 0.001)
    return folium.CircleMarker([random_lat, random_lon])

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

