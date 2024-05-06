#!/usr/bin/python3
"""this module defines the emergency contact model"""

# standard library import

# Third-party imports
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

# local imports
from app.models.base_model import BaseModel, Base


class EmergencyContact(BaseModel, Base):
    """emergency contacts table"""

    __tablename__ = "emergency_contacts"
    full_name: str = Column(String(128), nullable=False)
    phone: str = Column(String(60), unique=True, nullable=False)
    patient_id = Column(String, ForeignKey("patients.id", ondelete="CASCADE"))

    patient = relationship(
        "Patient", back_populates="emergency_contacts", foreign_keys=[patient_id]
    )
