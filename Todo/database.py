# Import necessary modules from SQLAlchemy

from sqlalchemy import create_engine  # * Used to create a connection to the database
from sqlalchemy.orm import sessionmaker  # * Helps in handling database sessions
from sqlalchemy.ext.declarative import declarative_base  # * Base class for all models

# ? Import dotenv to load environment variables from .env file
from dotenv import load_dotenv
import os

# * Load environment variables from the .env file
load_dotenv()

# * Get the database URL from the environment variables
# * This should be set in the .env file as:
# * DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/todo-fastapi"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# * Create the MySQL database engine
# * The engine is responsible for managing the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# * Create a database session factory
# * This session is used to interact with the database
SessionLocal = sessionmaker(autocommit=False,  # * Prevents automatic commits to avoid accidental changes
                            autoflush=False,   # * Prevents auto-flushing changes before commit
                            bind=engine)       # * Binds the session to the database engine

# * Create a Base class for defining database models
# * All database models should inherit from this Base class
Base = declarative_base()

# * Database dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()