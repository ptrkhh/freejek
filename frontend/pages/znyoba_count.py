from entities.constant import VEHICLE_CLASS_INDEX
import streamlit as st
vehicle_class: str = st.radio("Choose your vehicle class:", range(len(VEHICLE_CLASS_INDEX)), format_func=lambda x: VEHICLE_CLASS_INDEX[x])
st.write(vehicle_class)