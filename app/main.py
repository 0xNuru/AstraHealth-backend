from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patient
from app.routers import doctor
from app.routers import auth

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(auth.router)
