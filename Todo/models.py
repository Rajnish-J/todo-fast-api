from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Users(Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)  # * Added length (255)
    username = Column(String(100), nullable=False)  # * Added length (100)
    firstname = Column(String(100), nullable=False)  # * Added length (100)
    lastname = Column(String(100), nullable=False)  # * Added length (100)
    hashed_password = Column(String(255), nullable=False)  # * Added length (255)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False)  # * Added length (50)

class Todo(Base):
    __tablename__ = 'todos'
    
    todo_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # * Ensure lowercase "users"

    title = Column(String(255), nullable=False)  # * Added length (255)
    description = Column(String(500), nullable=True)  # * Added length (500)
    priority = Column(Integer, nullable=False)
    complete_status = Column(Boolean, default=False)
