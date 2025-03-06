from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv
import jwt

# * router to main.py for the API calling
router = APIRouter(prefix="/user", tags=["User"])

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# * Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# * function to check authenticated user or not
def authenticateUser(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

# * funtion to generate access token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm = ALGORITHM)

class UserRequest(BaseModel):
    email: str = Field(max_length=50)
    username: str = Field(max_length=30)
    firstname: str = Field(max_length=15)
    lastname: str = Field(max_length=15)
    password: str = Field(min_length=8, max_length=16)
    is_active: bool
    role: str = Field(max_length=15)

@router.post("/getAccessToken")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=45))
    
    return token

@router.post("/createUser", status_code=status.HTTP_201_CREATED)
async def createUser(create_user: UserRequest, db: Session = Depends(get_db)):
    hash_password = bcrypt_context.hash(create_user.password)
    user_obj = Users(
        email=create_user.email,
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        password=hash_password,
        is_active=create_user.is_active,
        role=create_user.role
    )

    if user_obj.is_active:
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
    else:
        raise HTTPException(status_code=404, detail="User is not active")


@router.get("/fetchuserbyid/{id}", status_code=status.HTTP_200_OK)
async def fetchuserbyid(id: int = Path(gt=0), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="No user found")
