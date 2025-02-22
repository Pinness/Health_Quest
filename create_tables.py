
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from new_app import db, app
from dotenv import load_dotenv
import os
#from models.base import Base
from models.user import User
from models.category import Category
from models.quiz import Quiz
from models.question import Question
from models.answer import Answer
from models.user_response import UserResponse

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URI')

if not DATABASE_URL:
        raise ValueError("Database URL not found. Ensure SQLALCHEMY_DATABASE_URI is set in your .env file.")

    # Create an SQLAlchemy engine
#engine = create_engine(DATABASE_URL, echo=True)

    # Create tables in the database
#Base.metadata.create_all(engine)

with app.app_context():
    db.create_all()
print("Tables created successfully!")

