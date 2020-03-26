import sys
import os
#for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime

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

#create declarative_base instance
Base = declarative_base()

#we'll add classes here
class User(Base):  
    __tablename__ = 'user'
    id = Column(Integer, Sequence('id', start=1, increment=1),primary_key=True)    
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)