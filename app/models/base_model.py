#!/usr/bin/python3
"""
This is the base_model inherited by all classes
contains:
    - methods:
        - save 
        - delete 
        - to_dict
        - __repr__ 
        - __str__ 
    - attributes:
        - id
        - created_at
        - updated_at
"""

import uuid
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """
        This class defines all common attributes/methods
        for other classes that would inherit it.
    """

    id = Column(String(200), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """
            Initialization of base model class

            Args:
                args: Not used
                Kwargs: constructor for the basemodel

            Attributes:
                id: unique id generated
                created_at: creation date
                updated_at: updated date
        """

        # check if parameters were passed as kwargs
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
                if "id" not in kwargs:
                    self.id = str(uuid.uuid4())
                if "created_at" not in kwargs:
                    self.created_at = datetime.now()
                if "updated_at" not in kwargs:
                    self.updated_at = datetime.now()

        else:
            self.id = str(uuid.uuid4())
            self.updated_at = self.created_at = datetime.now()

    def __str__(self):
        """
            This method defines the property of the class in a string fmt
            Return:
                returns a string containing of class name, id and dict
        """
        return self.__str__()

    def __repr__(self):
        """
            Return:
                returns a string representation of the calss

        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """This methods updates the updated_at attribute"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """
            This method creates a dictionary representation of the class

            Return:
                returns a dict rep of the class
        """

        base_dict = dict(self.__dict__)
        base_dict['__class__'] = str(type(self).__name__)
        base_dict['created_at'] = self.created_at.isoformat()
        base_dict['updated_at'] = self.updated_at.isoformat()

        return base_dict

