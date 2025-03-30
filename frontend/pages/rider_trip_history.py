import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium


@st.cache_data
def _get_all_state_bounds() -> dict:
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    return requests.get(url).json()


@st.cache_data
def get_state_bounds(state: str) -> dict:
    data = _get_all_state_bounds()
    state_entry = next(f for f in data["features"] if f["properties"]["name"] == state)
    return {"type": "FeatureCollection", "features": [state_entry]}

center = None
if "last_object_clicked" not in st.session_state:
    st.session_state["last_object_clicked"] = None
if st.session_state["last_object_clicked"]:
    center = st.session_state["last_object_clicked"]
if "selected_state" not in st.session_state:
    st.session_state["selected_state"] = "Indiana"
bounds = get_state_bounds(st.session_state["selected_state"])

m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

# If you want to dynamically add or remove items from the map,
# add them to a FeatureGroup and pass it to st_folium
fg = folium.FeatureGroup(name="State bounds")
fg.add_child(folium.features.GeoJson(bounds))

STATE_DATA = pd.read_csv("states.csv")
capitals = STATE_DATA

for capital in capitals.itertuples():
    fg.add_child(
        folium.Marker(
            location=[capital.latitude, capital.longitude],
            popup=f"{capital.capital}, {capital.state}",
            tooltip=f"{capital.capital}, {capital.state}",
            icon=folium.Icon(color="green")
            if capital.state == st.session_state["selected_state"]
            else None,
        )
    )

out = st_folium(
    m,
    feature_group_to_add=fg,
    center=center,
    width=1200,
    height=500,
)
