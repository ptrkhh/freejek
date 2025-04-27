import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from entities.latlon import LatLon

if "last_count" not in st.session_state:
    st.session_state["last_count"] = 0
count = st_autorefresh(interval=5000, key="fizzbuzzcounter")

trip = [LatLon(lat=52.517033, lon=13.388798), LatLon(lat=52.516848, lon=13.388827), LatLon(lat=52.517587, lon=13.39893),
        LatLon(lat=52.518873, lon=13.402702), LatLon(lat=52.527047, lon=13.415945),
        LatLon(lat=52.528458, lon=13.417166), LatLon(lat=52.528068, lon=13.424993),
        LatLon(lat=52.524964, lon=13.430405), LatLon(lat=52.523269, lon=13.429678),
        LatLon(lat=52.523239, lon=13.428554)]

fg = folium.FeatureGroup(name="Moving Marker")


pl = folium.PolyLine([i.as_tuple() for i in trip], tooltip="Coast")
fg.add_child(pl)

out = st_folium(
    folium.Map(location=trip[count % len(trip)].as_tuple(), zoom_start=16),
    feature_group_to_add=fg,
    # center=(center_lat, center_lon),
    # width=1200,
    # height=500,
)

st.text_input(label="something")

if count != st.session_state["last_count"]:
    last_count = count


