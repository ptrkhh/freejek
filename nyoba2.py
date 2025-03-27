import os
from typing import List
import streamlit as st
import streamlit
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session
from sqlmodel import select
from streamlit_local_storage import LocalStorage

from backend.entities.vehicle_model import VehicleModel

local_storage = LocalStorage()
local_storage.setItem("camera", "Tarah", key="camera5")
local_storage.setItem("camera2", "Tarah3", key="camera6")
local_storage.setItem("camera4", "Tarah5", key="camera7")



st.button("Click here")

st.info(local_storage.getItem("acdxx"))
# load_dotenv()
# engine = create_engine(os.environ.get("POSTGRES_URL"))
# sess = Session(engine)
# statement = select(VehicleModel)
# # results: List[VehicleModel] = sess.exec(statement).all()
# results: List[VehicleModel] = sess.exec(statement).all()
# print(results)
