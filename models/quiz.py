from flask_sqlalchemy import SQLAlchemy
from extensions import db

#from sqlalchemy import Column, Integer, String, Text, ForeignKey
#from sqlalchemy.orm import relationship
#from .base import Base


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_title = db.Column(db.String(50), nullable=False)
    quiz_description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)


    category = db.relationship('Category', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz')

    def __repr__(self):
        return f'<Quiz {self.quiz_title}>'
