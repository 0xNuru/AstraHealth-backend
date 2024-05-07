from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patient
from app.routers import doctor
from app.routers import auth

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pasebukky.github.io/", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello, World!"}


app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(auth.router)
