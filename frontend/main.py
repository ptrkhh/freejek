import streamlit as st
from streamlit_local_storage import LocalStorage

from backend.controller.router import Controller

c = Controller()

st.title("FREEJEK ALWAYS FREE")

st.session_state["local_storage"]: LocalStorage = LocalStorage()
