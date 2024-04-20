from fastapi import FastAPI
from app.routers import patient

app = FastAPI()

app.include_router(patient.router)