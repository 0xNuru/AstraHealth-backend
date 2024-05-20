#!/usr/bin/python3
"""This module contians the doctor-related endpoints"""
import base64
import binascii
from app.engine.load import load
from app.models.doctor import Doctor
from app.models.user import User
from app.schema.doctor import UpdateDoctorProfile, ShowDoctorProfile, ShowDoctorSchedule, ShowDoctorCard
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


@router.patch(
    "/update_profile", status_code=status.HTTP_200_OK
)
def update_profile(
    request: UpdateDoctorProfile,
    db: Session = Depends(load),
    user: Doctor = Depends(auth.get_current_user),
):
    doctor = db.query_eng(Doctor).filter(Doctor.id == user.id).first()
    for field, value in request.dict(exclude_unset=True).items():
        if value not in (None, ""):
            if field == "image":
                if value.startswith('data:image') and ';base64,' in value:
                    header, value = value.split(';base64,')
                # convert base64 image to binary
                try:
                    value = base64.b64decode(value)
                    setattr(doctor, "image_header", header)
                except binascii.Error:
                    raise HTTPException(
                        status_code=400, detail=[{"msg": "Invalid base64-encoded string for image"}]
                    )
            if field == "calendarLink":
                print('yes')
                if value.startswith('https://'):
                    protocol, value = value.split('https://cal.com/')
            if field == "gender":
                value = value.capitalize()

            setattr(doctor, field, value)

    db.add(doctor)
    return {"message": "Profile updated successfully!"}


@router.get(
    "/profile", response_model=ShowDoctorProfile, status_code=status.HTTP_200_OK
)
def profile(db: Session = Depends(load), user: User = Depends(auth.get_current_user)):
    doctor = db.query_eng(Doctor).filter(Doctor.id == user.id).first()
    image_base64 = base64.b64encode(doctor.image).decode('utf-8') if doctor.image else None
    if image_base64:
        image_base64 = f"{doctor.image_header};base64,{image_base64}"
    doctor_dict = {key: value for key, value in doctor.__dict__.items() if key != 'image'}

    return {
        **user.__dict__,
        **doctor_dict,
        "image": image_base64,
    }

@router.get("/all", response_model=List[ShowDoctorCard], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    doctors = db.query_eng(Doctor).all()
    for doctor in doctors:
        doctor.image = base64.b64encode(doctor.image).decode('utf-8') if doctor.image else None
        if doctor.image:
            doctor.image = f"{doctor.image_header};base64,{doctor.image}"
    return doctors

@router.get(
    "/{doctor_id}", response_model=ShowDoctorSchedule, status_code=status.HTTP_200_OK
)
def schedule(doctor_id, db: Session = Depends(load), user: User = Depends(auth.get_current_user)):
    doctor = db.query_eng(Doctor).filter(Doctor.id == doctor_id).first()
    doctor_details = db.query_eng(User).filter(User.email == doctor.email).first()
    image_base64 = base64.b64encode(doctor.image).decode('utf-8') if doctor.image else None
    if image_base64:
        image_base64 = f"{doctor.image_header};base64,{image_base64}"
    doctor_dict = {key: value for key, value in doctor.__dict__.items() if key != 'image'}

    return {
        **doctor_details.__dict__,
        **doctor_dict,
        "image": image_base64,
    }