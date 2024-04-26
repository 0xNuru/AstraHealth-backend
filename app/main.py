from fastapi import FastAPI
from app.routers import patient
from app.routers import doctor
from app.routers import auth

app = FastAPI()

app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(auth.router)
