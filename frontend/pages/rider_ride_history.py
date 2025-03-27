import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

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
