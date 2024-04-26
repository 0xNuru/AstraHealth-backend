#!/usr/bin/python3
"""
this module defines the schema for making requests 
and returning responses to the auth endpoints
"""

from pydantic import BaseModel, EmailStr, SecretStr


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class LoginResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    msg = "Login Successful"

    class Config:
        orm_mode = True
