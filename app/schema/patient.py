#!/usr/bin/python3
"""
this module defines the schema for making requests 
and returning responses to the patient endpoints
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, constr, validator

from app.models.patient import GenderEnum


class UpdatePatientProfile(BaseModel):
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    image: Optional[str] = None
    SOS_fullname: Optional[str] = None
    SOS_phone: Optional[constr(min_length=11, max_length=14)] = None # type: ignore

    @validator('SOS_phone', pre=True, always=True)
    def empty_str_to_none(cls, v):
        """
        This method is a validator for the 'SOS_phone' field in the UpdatePatientProfile model.
        It converts empty strings to None before assigning the value to the field.

        Parameters:
        cls (class): The class (in this case, UpdatePatientProfile) to which the validator is attached.
        v (str): The value to be validated.

        Returns:
        None or str: Returns None if the input value is an empty string, otherwise returns the input value.
        """
        return None if v == "" else v


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
