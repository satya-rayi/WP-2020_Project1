import os
import time  
import hashlib 

from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import User


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

@app.route("/admin")
def admin():
    users = db.query(User).order_by(User.created_at.desc()).all()
    return render_template('users.html',users=users)  

@app.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':        
        username = request.form['username']
        password = request.form["password"]
        password = hashlib.md5(password.encode()).hexdigest()
        
        exists = db.query(User.id).filter_by(username=username).scalar()
        if (exists is None) :
            user = User(username=username, password=password, created_at=time.strftime('%Y-%m-%d %H:%M:%S'))
            db.add(user)
            db.commit()
            return render_template('welcome.html',username=username)        
        username = ""
        return render_template('welcome.html',username=username)
    else:
        return render_template('register.html')

