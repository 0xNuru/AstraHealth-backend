#!/usr/bin/python3
"""
this module defines the schema for making requests 
and returning responses to the patient endpoints
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.patient import GenderEnum


class UpdatePatientProfile(BaseModel):
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    image: Optional[str] = None
    SOS_fullname: Optional[str] = None
    SOS_phone: Optional[str] = None

    class Config:
        orm_mode = True


class ShowPatientProfile(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    image: Optional[str] = None
    SOS_fullname: Optional[str] = None
    SOS_phone: Optional[str] = None

    class Config:
        orm_mode = True
