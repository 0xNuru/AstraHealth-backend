#!/usr/bin/python3
"""this module defines the patient model"""

from sqlalchemy import Column, ForeignKey, String

from app.models.user import User


class Patient(User):
    """patient table"""

    __tablename__ = "patients"
    id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
