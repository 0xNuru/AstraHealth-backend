#!/usr/bin/python3
"""
this module defines the schema for making requests 
and returning responses to the user endpoints
"""

import re

from datetime import date
from pydantic import BaseModel, EmailStr, SecretStr, constr, root_validator

from app.models.user import GenderEnum


password_regex = (
    "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"
)


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password1: SecretStr
    password2: SecretStr
    gender: GenderEnum
    dob: date
    phone: constr(min_length=11, max_length=14)  # type: ignore
    address: constr(min_length=10)  # type: ignore

    class Config:
        orm_mode = True

    @root_validator()
    def verify_password_match(cls, values):
        password1 = values.get("password1")
        password2 = values.get("password2")

        if password1 is None or password2 is None:
            raise ValueError("Both password fields must be provided.")

        password = password1.get_secret_value()
        confirm_password = password2.get_secret_value()

        if password != confirm_password:
            raise ValueError("The two passwords did not match.")

        if not re.match(password_regex, confirm_password):
            raise ValueError(
                "Password must be at least 8 characters and include alphabets, numbers, and a special character."
            )

        return values


class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
