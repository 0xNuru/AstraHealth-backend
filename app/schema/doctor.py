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
    medical_liscence: Optional[str] = None
    hospital_affiliation: Optional[str] = None
    resume_link: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True


class ShowDoctorProfile(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: str
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medical_liscence: Optional[str] = None
    hospital_affiliation: Optional[str] = None
    resume_link: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True
