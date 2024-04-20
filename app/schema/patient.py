#!/usr/bin/python3
"""
this module defines the schema for making requests 
and returning responsesto the endpoints
"""

import re


from datetime import date
from pydantic import BaseModel, EmailStr, SecretStr, constr, root_validator

from app.models.user import GenderEnum


password_regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"


class Patient(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password1: SecretStr
    password2: SecretStr
    gender: GenderEnum
    dob: date
    phone: constr(min_length=11, max_length=14) # type: ignore
    address: constr(min_length=10) # type: ignore

    class Config():
        orm_mode = True

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password1").get_secret_value()
        confirm_password = values.get("password2").get_secret_value()
        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        if not re.match(password_regex, confirm_password):
            raise ValueError(
                "Password length must be atleast 8 and contains alphabets, number with a spectial character")
        return values


class ShowPatient(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True