from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#from sqlalchemy.orm import relationship
#from .base import Base

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20))
    password = db.Column(db.String(128), nullable=False) # Store hashed password


    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password matches the hashed password"""
        return check_password_hash(self.password, password)
