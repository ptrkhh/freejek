import streamlit as st

from backend.controller.router import Controller

c = Controller()


# Function for the rider login page
def rider_login_page():
    st.title("Rider Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        success = c.rider_sign_in(username, password)
        if success:
            st.success("Successfully signed in as rider!")
        else:
            st.error("Invalid username or password.")


# Function for the driver login page
def driver_login_page():
    st.title("Driver Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        success = c.rider_sign_in(username, password)  # TODO replace with driver
        if success:
            st.success("Successfully signed in as driver!")
        else:
            st.error("Invalid username or password.")
