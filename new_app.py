from flask import Flask, render_template, request, redirect, session, url_for
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from dotenv import load_dotenv
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import DataRequired, Email, ValidationError
#from database import Base, User, Category, Quiz, Question, Answer, UserResponse, SessionLocal
from os import getenv # Helps to get the environmental variables
#import bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine



#from models import Base, User, Category, Quiz, Question, Answer, UserResponse


# Load environment variables from .env file
load_dotenv()

#initialise flask app
app = Flask(__name__)


# Construct the database URI
#db_url = getenv('SQLALCHEMY_DATABASE_URI')



# Configure Flask app
app.secret_key = getenv('FLASK_SECRET_KEY') # secret key for sessions
#db_url = getenv('SQLALCHEMY_DATABASE_URI') #database url
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#Instantiates the database connectionConfigure sqlalchemy to work with flask
                


# Set up SQLALCHEMY
#engine = create_engine(db_url)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base.metadata.create_all(bind=engine)
#print(db_url)

#Initialise Flask_SQLALchemy (used only for session management here)
db = SQLAlchemy(app)


# Initialise Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'signup'
login_manager.init_app(app)


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    categories = fetch_categories()
    return render_template('home.html', categories=categories)



@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        user = User.query.filter_by(username=username).first()
        if user:
            flash("User already exists!", "danger")
            return redirect(url_for("signup"))
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Signup successful! Welcome", "success")
            return redirect(url_for('dashboard'))
    return render_template("signup.html")


@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html', error="Invalid username or password")



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/categories', strict_slashes=False)
@login_required
def show_categories():
    categories = fetch_categories_with_quizzes()
    return render_template('categories.html', categories=categories)


@app.route('/quiz/<int:quiz_id>', strict_slashes=False)
def show_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz_title=quiz.quiz_title, quiz_description=quiz.quiz_description, quiz_id=quiz_id)



@app.route('/start_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    session['quiz_id'] = quiz_id
    session['current_question_index'] = 0
    session['user_response'] = []
    return render_template('quiz.html', quiz=quiz, question=questions[0], question_index=0)


@app.route('/next_question', methods=['POST'])
def next_question():
    quiz_id = session.get('quiz_id')
    current_question_index = session.get('current_question_index')
    question_id = request.form.get('question_id')
    selected_answer_id = request.form.get('selected_answer_id')
    selected_answer = Answer.query.get(selected_answer_id)
    is_correct = selected_answer.is_correct
    user_response = UserResponse(
            user_id=current_user.id,
            question_id=question_id,
            selected_answer_id=selected_answer_id,
            is_correct=is_correct
        )
    db.session.add(user_response)
    db.session.commit()

    current_question_index += 1
    session['current_question_index'] = current_question_index
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz = Quiz.query.get(quiz_id)

    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        return render_template('quiz.html', quiz=quiz, question=next_question, question_index=current_question_index)
    else:
        return redirect(url_for('end_quiz'))



@app.route('/end_quiz', methods=['GET'])
def end_quiz():
    quiz_id = session.get('quiz_id')
    user_responses = UserResponse.query.filter_by(user_id=current_user.id).all()
    total_questions = len(user_responses)
    correct_answers = sum([response.is_correct for response in user_responses])
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return render_template('quiz_end.html', score=score)



# Helper functions
def fetch_categories():
    return Category.query.all()


def fetch_categories_with_quizzes():
    categories = Category.query.all()    #db.session.query(Category).all()
    categories_list = []
    for category in categories:
        quizzes = Quiz.query.filter_by(category_id=category.category_id).all()
        quizzes_list = [{'quiz_id': quiz.quiz_id, 'quiz_title': quiz.quiz_title, 'quiz_description': quiz.quiz_description} for quiz in quizzes]
        category_info = {
                'id': category.category_id,
                'category_name': category.category_name,
                'category_description': category.category_description,
                'quizzes': quizzes_list
            }
        categories_list.append(category_info)
    return categories_list


# Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
