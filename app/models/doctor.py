#!/usr/bin/python3
"""this module defines the doctors model"""

import enum
from sqlalchemy import Column, Date, Enum, Float, ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship


from app.models.user import User


class GenderEnum(enum.Enum):
    M = "Male"
    F = "Female"


class Doctor(User):
    """doctor table"""

    __tablename__ = "doctors"
    id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    image = Column(LargeBinary, nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum, name="gender_enum"))
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    medical_liscence = Column(String(270), nullable=True)
    resume_link = Column(String(270), nullable=True)
    hospital_affiliation = Column(String(270), nullable=True)
    bio = Column(String(220), nullable=True)
