# Import necessary modules from SQLAlchemy
from database import Base  # * Import Base from database.py to define our models
from sqlalchemy import Column, Integer, String, Boolean  # * Import column types

# * Define the Todo model, which represents the 'todos' table in the database
class Todo(Base):
    # * Name of the table in the database
    __tablename__ = 'todos'  
    
    # * Define the columns of the table
    
    # * 'id' column: A unique identifier for each task (Primary Key)
    id = Column(Integer, primary_key=True, index=True)  # * Primary key ensures each row has a unique ID

    # * 'title' column: A short title for the task (VARCHAR with max length 255)
    title = Column(String(255), nullable=False)  # * String requires a length in MySQL

    # * 'description' column: A longer description for the task (VARCHAR with max length 500)
    description = Column(String(500), nullable=True)  # * Can be left empty (NULL allowed)

    # * 'priority' column: An integer to define the priority of the task (e.g., 1 = Low, 5 = High)
    priority = Column(Integer, nullable=False)  

    # * 'complete_status' column: A boolean value indicating if the task is completed or not
    complete_status = Column(Boolean, default=False)  # * Default value is False (Task is incomplete)
