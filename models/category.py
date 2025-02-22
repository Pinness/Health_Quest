from flask_sqlalchemy import SQLAlchemy
from extensions import db
#from sqlalchemy import Column, Integer, String, Text
#from sqlalchemy.orm import relationship
#from .base import Base

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    category_description = db.Column(db.Text)


    quizzes = db.relationship('Quiz', back_populates='category')
    
    def __repr__(self):
        return f'<ategory {self.category_name}>'
