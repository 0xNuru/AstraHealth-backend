#!/usr/bin/python3
"""This module contians the patient-related endpoints"""
from app.engine.load import load
from app.models.patient import Patient
from app.models.user import User
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
        gender=request.gender,
        address=request.address,
        dob=request.dob,
        phone=request.phone,
        email=request.email,
        password_hash=password_hash,
        role="patient",
    )
    db.add(new_patient)
    return new_patient


@router.get("/all", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    print(type(db))
    patients = db.query_eng(Patient).all()
    return patients
