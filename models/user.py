from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(20))
    password = Column(String(20), nullable=False)
