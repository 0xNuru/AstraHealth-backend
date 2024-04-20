#!/usr/bin/python3
"""this module defines the user model"""

#standard library import
import enum

#Third-party imports
from sqlalchemy import Column, String, Enum

#local imports
from models.base_model import BaseModel, Base


class GenderEnum(enum.Enum):
    M = "Male"
    F = "Female"


class Users(BaseModel, Base):
    """user table"""
    __tablename__ = "user"
    first_name: str = Column(String(128), nullable=False)
    last_name: str = Column(String(128), nullable=False)
    gender = Column(Enum(GenderEnum, name="gender_enum"))
    address: str = Column(String(256), nullable=False)
    phone: str = Column(String(60), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=True)
