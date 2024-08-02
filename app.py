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
        return check_password_hash(self.password_hash, password)


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


if __name__ == "__main__":
    app.run(debug=True)
