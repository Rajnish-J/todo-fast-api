from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(25), nullable=False)
    firstname = Column(String(25), nullable=False)
    lastname = Column(String(25), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), nullable=False)

class Todo(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  

    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    priority = Column(Integer, nullable=False)
    complete_status = Column(Boolean, default=False)
