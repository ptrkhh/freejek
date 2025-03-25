import os
from typing import List

from dotenv import load_dotenv
from sqlalchemy import create_engine

from backend.entities.vehicle_model import VehicleModel
from sqlmodel import select
from sqlmodel import Session

load_dotenv()
engine =  create_engine(os.environ.get("POSTGRES_URL"))
sess = Session(engine)
statement = select(VehicleModel)
# results: List[VehicleModel] = sess.exec(statement).all()
results: List[VehicleModel] = sess.exec(statement).all()
print(results)
