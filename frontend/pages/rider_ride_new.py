import folium
import streamlit as st
import random
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

st.title("Random Dot on Map")

# Auto-refresh every 5 seconds
if "refresh_count" not in st.session_state:
    st.session_state.refresh_count = 0  # Initialize refresh count

st.session_state.refresh_count = st_autorefresh(interval=1000, limit=None, key="map_refresh")

# Define map center
center_lat, center_lon = 39.949610, -75.150282

# Initialize session state for random marker
if "random_lat" not in st.session_state or "random_lon" not in st.session_state:
    st.session_state.random_lat = center_lat
    st.session_state.random_lon = center_lon

# Only update coordinates when refresh count changes
if st.session_state.refresh_count > 0:
    st.session_state.random_lat = center_lat + random.uniform(-0.01, 0.01)
    st.session_state.random_lon = center_lon + random.uniform(-0.01, 0.01)

# Create a new map
m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

# Add fixed marker
folium.Marker(
    [center_lat, center_lon], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# Add random marker
folium.CircleMarker(
    location=[st.session_state.random_lat, st.session_state.random_lon],
    radius=8,
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.6,
).add_to(m)

# Render the map
st_folium(m, width=725)
