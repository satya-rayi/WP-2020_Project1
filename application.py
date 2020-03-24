import os

from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__, template_folder='templates')

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form["password"]
         return render_template('welcome.html',username=username)
    else:
        return render_template('register.html')

