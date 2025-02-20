from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
# from .base import Base
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


# Construct the database URI
db_url = os.getenv('SQLALCHEMY_DATABASE_URI')

Base = declarative_base()  # An instance of the declarative_base class


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(20))
    password = Column(String(128), nullable=False) # Store hashed password


    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password matches the hashed password"""
        return check_password_hash(self.password, password)


class Answer(Base):
    __tablename__ = 'answers'

    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    ans_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship('Question', back_populates='answers')

    def __repr__(self):
        return f'<Answer {self.ans_text}>'


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), unique=True, nullable=False)
    category_description = Column(Text)


    quizzes = relationship('Quiz', back_populates='category')
    
    def __repr__(self):
        return f'<ategory {self.category_name}>'


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)


    quiz = relationship('Quiz', back_populates='questions')
    answers = relationship('Answer', back_populates='question')
    user_responses = relationship('UserResponse', back_populates='question')

    def __repr__(self):
        return f'<Question {self.tesxt}>'


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_title = Column(String(50), nullable=False)
    quiz_description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)


    category = relationship('Category', back_populates='quizzes')
    questions = relationship('Question', back_populates='quiz')

    def __repr__(self):
        return f'<Quiz {self.quiz_title}>'


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(20))
    password = Column(String(128), nullable=False) # Store hashed password


    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password matches the hashed password"""
        return check_password_hash(self.password, password)


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


try:
    engine = create_engine(DATABASE_URI, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
except:
    print("Error in table creation, connection failed)
