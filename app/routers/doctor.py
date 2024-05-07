#!/usr/bin/python3
"""This module contians the doctor-related endpoints"""
import base64
import binascii
from app.engine.load import load
from app.models.doctor import Doctor
from app.models.emergency_contact import EmergencyContact
from app.models.user import User
from app.schema.doctor import UpdateDoctorProfile, ShowDoctorProfile
from app.schema.user import ShowUser, CreateUser
from app.utils import auth
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/v1/doctor", tags=["doctor management"])


@router.get("/")
def root():
    return {"message": "Hello, World!"}


@router.post("/register", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def register(request: CreateUser, db: Session = Depends(load)):
    phone = request.phone
    email = request.email.lower()

    check_phone = db.query_eng(User).filter(User.phone == phone).first()
    check_email = db.query_eng(User).filter(User.email == email).first()

    if check_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": f"user with phone: {phone} exists"}],
        )
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": f"user with email: {email} exists"}],
        )
    password_hash = auth.get_password_hash(request.password1.get_secret_value())
    new_doctor = Doctor(
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        email=request.email,
        password_hash=password_hash,
        role="doctor",
    )
    db.add(new_doctor)
    return new_doctor


@router.get("/all", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    doctors = db.query_eng(Doctor).all()
    return doctors


@router.patch(
    "/update_profile", response_model=ShowDoctorProfile, status_code=status.HTTP_200_OK
)
def update_profile(
    request: UpdateDoctorProfile,
    db: Session = Depends(load),
    user: Doctor = Depends(auth.get_current_user),
):
    doctor = db.query_eng(Doctor).filter(Doctor.id == user.id).first()
    for field, value in request.dict(exclude_unset=True).items():
        if value is not None:
            if field == "image":
                # convert base64 image to binary
                try:
                    value = base64.b64decode(value)
                except binascii.Error:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid base64-encoded string for image",
                    )

            setattr(doctor, field, value)

    db.add(doctor)
    return {
        **user.__dict__,
        **doctor.__dict__,
    }


@router.get(
    "/profile", response_model=ShowDoctorProfile, status_code=status.HTTP_200_OK
)
def profile(db: Session = Depends(load), user: User = Depends(auth.get_current_user)):
    doctor = db.query_eng(Doctor).filter(Doctor.id == user.id).first()

    return {**user.__dict__, **doctor.__dict__}
