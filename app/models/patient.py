#!/usr/bin/python3
"""this module defines the patient model"""

import enum

from sqlalchemy import Column, ForeignKey, String, Date, Enum, Float, LargeBinary
from sqlalchemy.orm import relationship

from app.models.user import User


class GenderEnum(enum.Enum):
    M = "Male"
    F = "Female"


class Patient(User):
    """patient table"""

    __tablename__ = "patients"
    id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    image = Column(LargeBinary, nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum, name="gender_enum"))
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    medical_history = Column(String(270), nullable=True)
    image = Column(LargeBinary, nullable=True)
    image_header = Column(String, nullable=True)

    emergency_contacts = relationship("EmergencyContact", back_populates="patient")
