import time
import traceback

import streamlit as st

from frontend.utils.init import init

# from frontend.utils.nyoba import TEST, is_signed_in
# print("THE TEST", TEST)

c, t, l, tr = init()

if t.is_signed_in():
    st.switch_page("main.py")
# Session state initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'email' not in st.session_state:
    st.session_state.email = ""


def submit_email():
    email = st.session_state.email_input
    try:
        c.rider_sign_up(email)
        st.session_state.email = email
        st.session_state.step = 2
    except FileExistsError:
        st.info("Email already registered")
    except Exception as e:
        st.error("Sign-up failed. Please try again.")
        print(e)
        traceback.print_exc()


def verify_otp():
    otp = st.session_state.otp_input
    password = st.session_state.password_input
    try:
        access_token, refresh_token = c.rider_otp_verify(st.session_state.email, otp, password)
        print("THE ACCESS TOKEN", type(access_token), access_token)
        print("THE REFRESH TOKEN", type(refresh_token), refresh_token)
        t.store_token(access_token, refresh_token, "rider")
        st.success("Sign-up successful! Redirecting...")
        time.sleep(2)
        st.switch_page("main.py")
    except Exception as e:
        st.error("Sign-up failed. Please try again.")
        print(e)
        traceback.print_exc()


st.title("Sign Up")

if st.session_state.step == 1:
    st.text_input("Email", key="email_input")
    st.button("Sign Up", on_click=submit_email)

elif st.session_state.step == 2:
    st.write("An OTP has been sent to your email. Please enter it below:")
    st.text_input("Enter OTP", key="otp_input")
    st.text_input("Password", type="password", key="password_input")
    st.button("Verify OTP", on_click=verify_otp)
