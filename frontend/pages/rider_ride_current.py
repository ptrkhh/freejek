import streamlit as st
from backend.controller.router import Controller

controller: Controller = st.session_state.controller

last_trip:

# AVAILABLE:
# Searching for drivers...
#
# From: <ADDRESS>
# To: <ADDRESS>
# Fare: <INSERT FARE>
# Note: <SOME TEXT>
# (button: Edit Request)
#
# Map: Blue dot for you, light blue path, red ring for other drivers
#
#
# ACCEPTED:
# Watch out for...
# <car picture>
# Car: <color> <type>
# Phone: <phone> <WA link> <telegram link>
# Note:
#
#
# Your Note: <SOME TEXT>
# (button: Edit Request)
#
# Map: Blue dot for you, light blue path, red dot for the driver
#
#
# ONGOING:
# You are xx % there! (time percentage vs. distance percentage, whichever lowest)
#
# Note: <SOME TEXT>
# Your Note: <SOME TEXT>
# (button: Edit Request)
#
# Map: Blue dot for you, light blue path, red dot for the driver
#
#
# COMPLETED:
# Congratulations! Trip has been completed!
#
# From: <ADDRESS>
# To: <ADDRESS>
# Fare: <INSERT FARE>
#
#
#
# CANCELED:
#
# Trip has been canceled!
#
# Note from you: <INSERT NOTE>
# Note from driver: <INSERT NOTE>
#
