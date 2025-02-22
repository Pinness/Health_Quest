from flask_sqlalchemy import SQLAlchemy
from extensions import db

#from sqlalchemy import Column, Integer, String, Text, ForeignKey
#from sqlalchemy.orm import relationship
#from .base import Base


class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)


    quiz = db.relationship('Quiz', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question')
    user_responses = db.relationship('UserResponse', back_populates='question')

    def __repr__(self):
        return f'<Question {self.tesxt}>'
