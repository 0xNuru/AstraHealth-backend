#!/usr/bin/python3
"""
this module defines the schema for making requests 
and returning responses to the patient endpoints
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.doctor import GenderEnum


class UpdateDoctorProfile(BaseModel):
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medicalLicense: Optional[str] = None
    hospitalAffiliation: Optional[str] = None
    resumeLink: Optional[str] = None
    professionalBio: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True


class ShowDoctorProfile(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medicalLicense: Optional[str] = None
    hospitalAffiliation: Optional[str] = None
    resumeLink: Optional[str] = None
    professionalBio: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True
