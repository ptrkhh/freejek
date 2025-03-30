import folium
import streamlit as st
from streamlit_folium import st_folium

center_lat, center_lon = 39.949610, -75.150282

if "random_lat" not in st.session_state or "random_lon" not in st.session_state:
    st.session_state.random_lat = center_lat
    st.session_state.random_lon = center_lon
m = folium.Map(location=[center_lat, center_lon], zoom_start=16)
folium.CircleMarker([st.session_state.random_lat, st.session_state.random_lon]).add_to(m)
st_folium(m, width=725)
