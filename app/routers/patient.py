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
    "/update_profile", status_code=status.HTTP_200_OK
)
def update_profile(
    request: UpdatePatientProfile,
    db: Session = Depends(load),
    user: Patient = Depends(auth.get_current_user),
):
    patient = db.query_eng(Patient).filter(Patient.id == user.id).first()
    for field, value in request.dict(exclude_unset=True).items():
        if value not in (None, ""):
            if field == "image":
                if value.startswith('data:image') and ';base64,' in value:
                    header, value = value.split(';base64,')
                # convert base64 image to binary
                try:
                    value = base64.b64decode(value)
                    setattr(patient, "image_header", header)
                except binascii.Error:
                    raise HTTPException(
                        status_code=400, detail=[{"msg": "Invalid base64-encoded string for image"}]
                    )

            setattr(patient, field, value)


    sos_contact =  db.query_eng(EmergencyContact).filter(EmergencyContact.patient_id == user.id).first()
    if sos_contact:
        if request.SOS_fullname:
            sos_contact.full_name = request.SOS_fullname
        if request.SOS_phone:
            sos_contact.phone = request.SOS_phone
            db.add(sos_contact)
    else:    
        if request.SOS_fullname and request.SOS_phone:
            sos_contact = EmergencyContact(
                full_name=request.SOS_fullname,
                phone=request.SOS_phone,
                patient_id=user.id,
                role="SOS_contact",
            )
            db.add(sos_contact)
            

    db.add(patient)
    return {"message": "Profile updated successfully!"}

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
    image_base64 = base64.b64encode(patient.image).decode('utf-8') if patient.image else None
    if image_base64:
        image_base64 = f"{patient.image_header};base64,{image_base64}"
    patient_dict = {key: value for key, value in patient.__dict__.items() if key != 'image'}

    return {
        **user.__dict__,
        **patient_dict,
        "image": image_base64,
        "SOS_fullname": sos_contact.full_name if sos_contact else None,
        "SOS_phone": sos_contact.phone if sos_contact else None,
    }
