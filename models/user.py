from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from .base import Base

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(20))
    password = Column(String(128), nullable=False) # Store hashed password


    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password matches the hashed password"""
        return check_password_hash(self.password, password)
