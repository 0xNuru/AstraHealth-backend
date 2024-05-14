#!/usr/bin/python3
"""This module contians the patient-related endpoints"""
import base64
import binascii
from app.engine.load import load
from app.models.patient import Patient
from app.models.emergency_contact import EmergencyContact
from app.models.user import User
from app.schema.patient import UpdatePatientProfile, ShowPatientProfile
from app.schema.user import ShowUser, CreateUser
from app.utils import auth
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/v1/patient", tags=["patient management"])


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
    new_patient = Patient(
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        email=request.email,
        password_hash=password_hash,
        role="patient",
    )
    db.add(new_patient)
    return new_patient


@router.patch(
    "/update_profile", response_model=ShowPatientProfile, status_code=status.HTTP_200_OK
)
def update_profile(
    request: UpdatePatientProfile,
    db: Session = Depends(load),
    user: Patient = Depends(auth.get_current_user),
):
    patient = db.query_eng(Patient).filter(Patient.id == user.id).first()
    for field, value in request.dict(exclude_unset=True).items():
        if value is not None and value is not "":
            if field == "image":
                # convert base64 image to binary
                try:
                    value = base64.b64decode(value)
                except binascii.Error:
                    raise HTTPException(
                        status_code=400, detail="Invalid base64-encoded string for image"
                    )

            setattr(patient, field, value)

    if request.SOS_phone is not None:
        sos_contact = EmergencyContact(
            full_name=request.SOS_fullname,
            phone=request.SOS_phone,
            patient_id=user.id,
            role="SOS_contact",
        )
        db.add(sos_contact)

    db.add(patient)
    return patient


@router.get(
    "/profile", response_model=ShowPatientProfile, status_code=status.HTTP_200_OK
)
def profile(db: Session = Depends(load), user: User = Depends(auth.get_current_user)):
    patient = db.query_eng(Patient).filter(Patient.id == user.id).first()
    sos_contact = (
        db.query_eng(EmergencyContact)
        .filter(EmergencyContact.patient_id == user.id)
        .first()
    )

    return {
        **user.__dict__,
        **patient.__dict__,
        "SOS_fullname": sos_contact.full_name if sos_contact else None,
        "SOS_phone": sos_contact.phone if sos_contact else None,
    }
