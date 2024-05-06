#!/usr/bin/python3
"""this module defines the user model"""

# standard library import

# Third-party imports
from sqlalchemy import Column, String

# local imports
from app.models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """user table"""

    __tablename__ = "users"
    first_name: str = Column(String(128), nullable=False)
    last_name: str = Column(String(128), nullable=False)
    # address: str = Column(String(256), nullable=False)
    phone: str = Column(String(60), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False)
