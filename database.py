from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Construct the database URI
db_url = os.getenv('SQLALCHEMY_DATABASE_URI')

Base = declarative_base()  # An instance of the declarative_base class

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username =  Column(String(20), unique=True, nullable=False)
    email = Column(String(20))
    password = Column(String(20), nullable=False)
    

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), unique=True, nullable=False)
    category_description = Column(Text)

    quizzes = relationship('Quiz', back_populates='categories')


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_title = Column(String(50), nullable=False)
    quiz_description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    
    category = relationship('Category', back_populates='quizzes')
    questions = relationship('Question', back_populates='quiz')


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)

    quiz = relationship('Quiz', back_populates='questions')
    answers = relationship('Answer', back_populates='question')
    user_responses = relationship('UserResponse', back_populates='question')


class Answer(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    ans_text = Column(Text, nullable=False)

    question = relationship('Question', back_populates='answers')


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



# user = User(id=3, name='Martin')
# session.add(user)
# session.commit()

# for state in session.query(User).all():
#     print("{}: {}".format(state.id, state.name))
# session.close()