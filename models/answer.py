from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Answer(Base):
    __tablename__ = 'answers'

    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    ans_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship('Question', back_populates='answers')

    def __repr__(self):
        return f'<Answer {self.ans_text}>'
