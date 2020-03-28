import os
import time  

from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_login import login_required, logout_user, current_user, login_user

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Users, Books

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

def datetimeformat(value):    
  return value.strftime("%d-%m-%Y, %H:%M:%S")

app.jinja_env.globals.update(datetimeformat=datetimeformat)

@app.route("/")
def index():
  return "Project 1: TODO"

@app.route("/auth" , methods=['POST'])
def auth():
  session["message"] = ""
  if request.method == 'POST':        
    username = request.form['username']
    password = request.form["password"]           
    user = db.query(Users).filter_by(username=username).first()  # Validate Login Attempt
    if user and user.check_password(password) :
      session["user"] = user
      return redirect(url_for('home'))
    session["message"] = "Wrong username/password"
    return redirect(url_for('register'))
  else:
    return render_template('register.html',message="Wrong username/password")

@app.route("/home")
def home():
  if session.get('user'):
    return render_template('user.html',username=session["user"].username)
  return redirect(url_for('register'))

@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for('register'))

@app.route("/admin")
def admin():
  users = db.query(Users).order_by(Users.created_at.desc()).all()
  return render_template('users.html',users=users)  

@app.route("/books")
def books():
  books = db.query(Books).order_by(Books.created_at.desc()).all()
  return render_template('books.html',books=books)  

@app.route("/deleteusers")
def deleteusers():
  db.query(Users).filter_by(username="satyawin008").delete()
  db.commit()
  return redirect(url_for('admin'))

@app.route('/register', methods=['GET', 'POST']) 
def register():
  if request.method == 'POST':
    session["message"] = ""       
    username = request.form['username']
    password = request.form["password"]

    try:
      user = Users(username=username, password=password)
      user.set_password(password)
      db.add(user)
      db.commit()
      return render_template('welcome.html',username=username)
    except IntegrityError:
      session["message"] = "User Already Exists" 
      return render_template('register.html') 

  else:
    return render_template('register.html')

