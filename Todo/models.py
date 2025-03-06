from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)  # * Added length (50)
    username = Column(String(25), nullable=False)  # * Added length (25)
    firstname = Column(String(25), nullable=False)  # * Added length (25)
    lastname = Column(String(25), nullable=False)  # * Added length (25)
    password = Column(String(25), nullable=False)  # * Added length (25)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), nullable=False)  # * Added length (20)

class Todo(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # * Ensure lowercase "users"

    title = Column(String(150), nullable=False)  # * Added length (150)
    description = Column(String(500), nullable=True)  # * Added length (500)
    priority = Column(Integer, nullable=False)
    complete_status = Column(Boolean, default=False)
