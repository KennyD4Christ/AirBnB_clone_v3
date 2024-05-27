#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv  # noqa
import sqlalchemy  # noqa
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.password = kwargs['password']

    @staticmethod
    def hash_password(password):
        """Hashes the password with MD5"""
        return hashlib.md5(password.encode()).hexdigest()

    @password.setter
    def password(self, value):
        """Setter for password"""
        self._password = self.hash_password(value)

    def to_dict(self):
        """Returns a dictionary representation of the User object"""
        # Get the dictionary representation from the BaseModel
        user_dict = super().to_dict()
        # Remove the password key from the dictionary
        user_dict.pop('password', None)
        return user_dict
