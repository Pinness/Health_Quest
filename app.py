from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
#from database import Base, User, Category, Quiz, Question, Answer, UserResponse, SessionLocal
from os import getenv # Helps to get the environmental variables
import bcrypt



# Load environment variables from .env file
load_dotenv()

# Construct the database URI
db_url = getenv('SQLALCHEMY_DATABASE_URI')


app = Flask(__name__)


# Getting the secret key
app.secret_key = getenv('FLASK_SECRET_KEY')
# Creating the database instance
app.config['SQLALCHEMY_DATABASE_URI'] = db_url  #Instantiates the database connectionConfigure sqlalchemy to work with flask

class RegisterForm(FlaskForm):
    name  = StringField("Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = StringField("Password",validators=[DataRequired()])
    submit = SubmitField("Register")

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Configure Flask app
#app.config['SECRET_KEY'] = getenv('FLASK_SECRET_KEY', 'default_secret_key')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    #def __init__(self, name, email, password_hash):
        #self.name = name
        #self.email = email
        #self.password_hash = password_hash

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route('/login', methods=["POST"]) #snce we're sending its post
def login():
    # Collect necessary info from form
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username  #creating a unique sssion for the user
        return redirect(url_for('dashboard'))
    else:
        return render_template('home.html')


#Register
@app.route("/register", methods=["POST"])

def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = User.query.filter_by(username=username).first()
    #doing some checks that the user is not already in the database
    if user:
        return render_template("home.html", error="User already here!")
    else:
        #create a new user and set email and password fields
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # This sets the hashed password
        
        # Add the new user to the database session and commit
        db.session.add(new_user)
        db.session.commit()

        #create a new session for the user
        session['username'] = username
        #redirect the user to the dashboard
        return redirect(url_for('dashboard'))

    # If the user is not in the database, show the home page
    return render_template("home.html")

@app.route('/')
def home():
    if "username" in session: #This means that they are logged in
        return redirect(url_for('dashboard'))  #dashboard shouldshow not the home page
    return render_template('home.html') #otherwise return the home page

"""
@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #store data in database

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
"""




@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html', username=session["username"])
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


class UserResponse(db.Model):
    __tablename__ = 'user_response'

    user_response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    selected_answer_id = db.Column(db.Integer, db.ForeignKey('answers.answer_id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    
    question = db.relationship('Question', back_populates='user_responses')
    selected_answer = db.relationship('Answer')
    user = db.relationship('User')


class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    category_description = db.Column(db.Text)
    
    quizzes = db.relationship('Quiz', back_populates='category')
    
    def __repr__(self):
        return f'<Category {self.category_name}>'




class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_title = db.Column(db.String(100), nullable=False, unique=True)
    quiz_description= db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    
    category = db.relationship('Category', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz')


    def __repr__(self):
        return f'<Quiz {self.quiz_title}>'



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
        return f'<Question {self.text}>'


class Answer(db.Model):
    __tablename__ = 'answers'
    
    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    ans_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)  # Add this line

    question = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return f'<Answer {self.is_correct}>'



# class UserResponse(db.Model):
#     __tablename__ = 'user_response'
# 
#     user_response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
#     selected_answer_id = db.Column(db.Integer, db.ForeignKey('answers.answer_id'), nullable=False)
#     is_correct = db.Column(db.Boolean, nullable=False)
#     
#     question = db.relationship('Question', back_populates='user_responses')
#     selected_answer = db.relationship('Answer')
#     user = db.relationship('User')



if __name__ == "__main__":
    app.run(debug=True)
