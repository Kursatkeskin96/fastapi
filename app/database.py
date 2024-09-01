import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Properly calling os.getenv() to load environment variables
# SQLALCHEMY_DATABASE_URL= 'postgresql://postgres:masterpw123@localhost:5433/postgres'
# AWS Conn
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:masterpw123@conference-db.cd26y20q6nb7.eu-north-1.rds.amazonaws.com:5432/postgres'


# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
