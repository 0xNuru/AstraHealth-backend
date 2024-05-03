#!/usr/bin/python3
"""this module defines the doctors model"""

from sqlalchemy import Column, ForeignKey, String

from app.models.user import User


class Doctor(User):
    """doctor table"""

    __tablename__ = "doctors"
    id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
