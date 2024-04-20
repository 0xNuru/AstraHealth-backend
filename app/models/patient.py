#!/usr/bin/python3
"""this module defines the patient model"""
import enum

from sqlalchemy import Column, ForeignKey, Enum, String

from models.user import Users


class Patient(Users):
    """patient table"""
    __tablename__ = "patients"
    id = Column(String, ForeignKey(
    'user.id',  ondelete="CASCADE"), primary_key=True)