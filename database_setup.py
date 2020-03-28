import sys
import os
import datetime
from alembic import op
#for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

#for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

#for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#create declarative_base instance
Base = declarative_base()

#we'll add classes here
class Users(Base):  
    __tablename__ = 'users'
    id = Column(Integer, Sequence('id', start=1, increment=1),primary_key=True)    
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint('username', name='_username_uc'),)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

#we'll add classes here
class Books(Base): 
		#isbn,title,author,year
    __tablename__ = 'books'
    id = Column(Integer, Sequence('id', start=1, increment=1),primary_key=True)    
    isbn = Column(String)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    

Base.metadata.create_all(engine)