from flask_sqlalchemy import SQLAlchemy
from extensions import db
#from sqlalchemy.orm import relationship
#from .base import Base



class Answer(db.Model):
    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    ans_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return f'<Answer {self.ans_text}>'
