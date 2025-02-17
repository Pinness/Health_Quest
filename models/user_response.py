from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserResponse(Base):
    __tablename__ = 'user_response'

    user_response_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    selected_answer_id = Column(Integer, ForeignKey('answers.answer_id'), nullable=False)
    is_correct = Column(Boolean, nullable=False)


    question = relationship('Question', back_populates='user_responses')
    selected_answer = relationship('Answer')
    user = relationship('User')
