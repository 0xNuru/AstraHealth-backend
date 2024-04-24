#!/usr/bin/python3
"""This module contians the patient-related endpoints"""
from app.engine.load import load
from fastapi import APIRouter, Depends, status
from app.models.patient import Patient
from app.schema.patient import ShowPatient
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/v1/patient", tags=["patient management"])


@router.get("/")
def root():
    return {"message": "Hello, World!"}


@router.get("/all", response_model=List[ShowPatient], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    patients = db.query_eng(Patient).all()
    return patients
