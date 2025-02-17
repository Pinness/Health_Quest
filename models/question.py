from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)


    quiz = relationship('Quiz', back_populates='questions')
    answers = relationship('Answer', back_populates='question')
    user_responses = relationship('UserResponse', back_populates='question')
