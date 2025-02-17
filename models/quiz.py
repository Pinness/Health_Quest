from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_title = Column(String(50), nullable=False)
    quiz_description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)


    category = relationship('Category', back_populates='quizzes')
    questions = relationship('Question', back_populates='quiz')
