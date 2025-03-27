import streamlit as st
from streamlit_local_storage import LocalStorage

ACCESS_TOKEN = "freejek_access_token"
REFRESH_TOKEN = "freejek_refresh_token"
TEST="icle"


ls: LocalStorage = LocalStorage()

def is_signed_in():
    if ACCESS_TOKEN in st.session_state and REFRESH_TOKEN in st.session_state:
        # TODO validate token
        return True
    if ls.getItem(ACCESS_TOKEN) and ls.getItem(REFRESH_TOKEN):
        # TODO validate token
        return True
    ls.eraseItem(ACCESS_TOKEN)
    ls.eraseItem(REFRESH_TOKEN)
    return False