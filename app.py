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
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


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

# Initialize the LoginManager instance
login_manager = LoginManager()

# This tells Flask-Login to redirect to this view if a user tries to access a protected page without being authenticated
login_manager.login_view = 'login'

# This binds the LoginManager to the Flask app so that it can manage user sessions
login_manager.init_app(app)



# Define the User model
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(100), nullable=False, unique=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
# 
#     #def __init__(self, name, email, password_hash):
#         #self.name = name
#         #self.email = email
#         #self.password_hash = password_hash
# 
#     def set_password(self, password):
#         self.password = generate_password_hash(password)
# 
#     def check_password(self, password):
#         return check_password_hash(self.password, password)

class User(db.Model, UserMixin):  # Inherit UserMixin
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)



@login_manager.user_loader
def load_user(id):
    # Retrieve the user from the database using the user_id
    return User.query.get(int(id))
      

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





# @app.route('/login', methods=["POST"]) #snce we're sending its post
# def login():
#     # Collect necessary info from form
#     username = request.form['username']
#     password = request.form['password']
#     user = User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         session['username'] = username  #creating a unique sssion for the user
#         return redirect(url_for('dashboard'))
#     else:
#         return render_template('login.html')
# 

@app.route('/login', methods=["POST"])
#@login_required
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)  # Use Flask-Login's login_user function
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    else:
        return render_template('login.html', error="Invalid username or password")  # Reload login with error message


#Register
@app.route("/signup", methods=["GET", "POST"])
#@login_required

def signup():
    if request.method == "POST":
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
    return render_template("signup.html")

# @app.route('/')
# def home():
#     if "username" in session: #This means that they are logged in
#         return redirect(url_for('dashboard'))  #dashboard shouldshow not the home page
# 
#     # Fetch categories without quizzes
#     categories = fetch_categories()
# 
#     # Pass the categories to the template
#     return render_template('home.html', categories=categories) #otherwise return the home page

@app.route('/')
#@login_required

def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    categories = fetch_categories()
    return render_template('home.html', categories=categories)

def fetch_categories():
    """
    Retrieves categories without their associated quizzes from the database.
    
    Returns:
        List of Category objects.
    """
    return Category.query.all()




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




# @app.route('/dashboard')
# def dashboard():
#     if "username" in session:
#         return render_template('dashboard.html', username=session["username"])
#     return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('home'))

@app.route('/logout')
#@login_required
def logout():
    logout_user()  # Use Flask-Login's logout_user function
    return redirect(url_for('home'))




@app.route('/categories', strict_slashes=False)
def show_categories():
    """
    Fetches the list of categories and their associated quizzes from the database.
    Renders the HTML template to display the categories with their quizzes.

    Returns:
        Rendered HTML template for the categories page, including category and quiz data.
    """
    # Fetch categories with associated quizzes from the database
    categories = fetch_categories_with_quizzes()
    
    # Render the 'categories.html' template, passing the categories data to the template
    return render_template('categories.html', categories=categories)

def fetch_categories_with_quizzes():
    """
    Retrieves categories and their associated quizzes from the database.
    Constructs a list of categories, each containing a list of associated quizzes.
    
    Returns:
        List of dictionaries, each containing category details and associated quizzes.
    """
    # Query the database to fetch all categories
    categories = Category.query.all()
    
    # Initialize an empty list to store category data along with quizzes
    categories_list = []
    
    # Iterate over each category fetched from the database
    for category in categories:
        # Query the database to fetch quizzes associated with the current category
        quizzes = Quiz.query.filter_by(category_id=category.category_id).all()
        
        # Initialize an empty list to store quizzes data for the current category
        quizzes_list = []
        
        # Iterate over each quiz associated with the current category
        for quiz in quizzes:
            # Create a dictionary with quiz details and add it to the quizzes list
            quizzes_list.append({
                'quiz_id': quiz.quiz_id,
                'quiz_title': quiz.quiz_title,
                'quiz_description': quiz.quiz_description
            })
        
        # Create a dictionary with category details and associated quizzes
        category_info = {
            'id': category.category_id,
            'category_name': category.category_name,
            'category_description': category.category_description,
            'quizzes': quizzes_list
        }
        
        # Add the category information to the categories list
        categories_list.append(category_info)
    
    # Return the list of categories with associated quizzes
    return categories_list





    

#Define routes for displaying categories
# @app.route('/categories', strict_slashes=False)
# def show_categories():
#     #Fetch the list of categories from the database
#     categories = fetch_categories_from_database()
# 
#     # Render the HTML template to display the categories
#     return render_categories_page(categories)
# 
# 
# # Fetch Categories from the database
# def fetch_categories_from_database():
#     # Query all categories from the database
#     categories = Category.query.all()
# 
#     # convert the query results into a list of dictionaries
#     categories_list = []
#     for category in categories:
#         category_info = {
#             'id': category.category_id,
#             'category_name': category.category_name,
#             'category_description': category.category_description
#         }
#         categories_list.append(category_info)
# 
#     # Return the list of category dictionaries
#     return categories_list
# 
# # Render the Categories Page
# def render_categories_page(categories_data):
#     # Generate the category html page
#     return render_template('categories.html', categories=categories_data)
# 

    


@app.route('/quiz/<int:quiz_id>', strict_slashes=False)
def show_quiz(quiz_id):
    """
    Fetches the details of a specific quiz based on the quiz_id.
    Renders the HTML template to display the quiz details.

    Args:
        quiz_id (int): The ID of the quiz to display.

    Returns:
        Rendered HTML template for the quiz details page.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz_title=quiz.quiz_title, quiz_description=quiz.quiz_description, quiz_id=quiz_id)


@app.route('/start_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def start_quiz(quiz_id):
    """
    Initiates the quiz for a given quiz ID and sets up the initial state for the quiz session.

    This route handles both 'GET' and 'POST' requests. It performs the following steps:
    1. Retrieves the quiz details and associated questions from the database using the provided quiz ID.
    2. Initializes session data to track the current state of the quiz.
    3. Renders the quiz start page with the first question of the quiz.

    Parameters:
        quiz_id (int): The ID of the quiz to be started.

    Returns:
        Rendered HTML template 'quiz.html' with the following context:
            - quiz: The quiz object containing quiz details.
            - question: The first question of the quiz.
            - question_index: The index of the current question (initially 0).
    """
    # Fetch the quiz details from the database using the provided quiz ID.
    # If the quiz with the specified ID does not exist, a 404 error is returned.
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Retrieve all questions associated with the specified quiz.
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Initialize session data to track the quiz state:
    # - 'quiz_id': Store the ID of the quiz being taken.
    # - 'current_question_index': Keep track of the index of the current question (starts at 0).
    # - 'user_responses': List to store the user's responses as they progress through the quiz.
    session['quiz_id'] = quiz_id
    session['current_question_index'] = 0
    session['user_responses'] = []
    
    # Render the 'quiz.html' template to display the quiz.
    # Pass the following context to the template:
    # - quiz: The quiz details.
    # - question: The first question of the quiz.
    # - question_index: The index of the current question (0, indicating the first question).
    return render_template('quiz.html', quiz=quiz, question=questions[0], question_index=0)



@app.route('/next_question', methods=['POST'])
def next_question():
    """
    Handles moving to the next question in the quiz, records the user's answer, and manages quiz progression.

    This route is triggered when the user submits an answer for the current question. It performs the following steps:
    1. Retrieves the quiz ID and current question index from the session.
    2. Records the user's answer and updates the database.
    3. Advances to the next question and updates the session state.
    4. Renders the template for the next question or redirects to the end of the quiz if it is the last question.

    Returns:
        Rendered HTML template 'quiz.html' with the next question if there are more questions.
        Redirects to the 'end_quiz' route if the quiz is finished.
    """
    # Retrieve the quiz ID and current question index from the session.
    quiz_id = session.get('quiz_id')
    current_question_index = session.get('current_question_index')
    
    # Retrieve the current question ID and selected answer ID from the form data.
    question_id = request.form.get('question_id')
    selected_answer_id = request.form.get('selected_answer_id')
    
    # Fetch the answer object from the database using the selected answer ID.
    selected_answer = Answer.query.get(selected_answer_id)
    
    # Determine if the selected answer is correct.
    is_correct = selected_answer.is_correct
    
    # Create a new UserResponse object to record the user's response.
    user_response = UserResponse(
        user_id=current_user.id,            # Current user's ID (assumes user is logged in).
        question_id=question_id,            # ID of the current question.
        selected_answer_id=selected_answer_id,  # ID of the selected answer.
        is_correct=is_correct               # Boolean indicating if the answer is correct.
    )
    
    # Add the UserResponse object to the database session and commit the transaction.
    db.session.add(user_response)
    db.session.commit()
    
    # Increment the current question index to move to the next question.
    current_question_index += 1
    session['current_question_index'] = current_question_index
    
    # Retrieve all questions for the current quiz from the database.
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    # Fetch the quiz object from the database.
    quiz = Quiz.query.get(quiz_id)
    
    # Check if there are more questions to display.
    if current_question_index < len(questions):
        # Fetch the next question based on the updated index.
        next_question = questions[current_question_index]
        
        # Render the 'quiz.html' template with the next question and updated index.
        return render_template('quiz.html', quiz=quiz, question=next_question, question_index=current_question_index)
    else:
        # If there are no more questions, redirect to the end of the quiz page.
        return redirect(url_for('end_quiz'))


@app.route('/end_quiz', methods=['GET'])
def end_quiz():
    """
    Ends the quiz, calculates the user's score, and displays the result.

    This route is triggered when the quiz is finished. It performs the following steps:
    1. Retrieves the quiz ID from the session.
    2. Fetches all user responses for the current user from the database.
    3. Calculates the user's score based on the number of correct answers.
    4. Renders the 'quiz_end.html' template to display the user's score.

    Returns:
        Rendered HTML template 'quiz_end.html' with the user's score.
    """
    # Retrieve the quiz ID from the session to ensure the correct quiz is referenced.
    quiz_id = session.get('quiz_id')
    
    # Fetch all user responses for the current user from the database.
    # This assumes the current user is logged in and `current_user` is available.
    user_responses = UserResponse.query.filter_by(user_id=current_user.id).all()
    
    # Calculate the total number of questions answered.
    total_questions = len(user_responses)
    
    # Calculate the number of correct answers by summing up the `is_correct` field.
    correct_answers = sum([response.is_correct for response in user_responses])
    
    # Compute the score as a percentage of correct answers.
    # If there are no questions, the score is set to 0.
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Render the 'quiz_end.html' template, passing the calculated score.
    return render_template('quiz_end.html', score=score)













if __name__ == "__main__":
    app.run(debug=True)
