# * Import Base from the database file to link our model to the database
from database import Base

# ? Import necessary SQLAlchemy components for defining the table schema
from sqlalchemy import Column, Integer, String, Boolean

# * Define the Todo class which represents a database table
class Todo(Base):
    # ?Set the name of the table in the database
    __tablename__ = 'todos'
    
    # * Define the columns in the table with their types and constraints
    
    # * Unique identifier for each to-do item (Primary Key)
    id = Column(Integer, primary_key=True, index=True)

    # * Title of the to-do item (Short description)
    title = Column(String)

    # * Detailed description of the to-do item
    description = Column(String)

    # * Priority level of the task (e.g., 1 = Low, 5 = High)
    priority = Column(Integer)

    # * Status of the to-do (True = Completed, False = Not Completed), default is False
    complete_status = Column(Boolean, default=False)
