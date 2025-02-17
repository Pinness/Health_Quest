from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), unique=True, nullable=False)
    category_description = Column(Text)


    quizzes = relationship('Quiz', back_populates='categories')

