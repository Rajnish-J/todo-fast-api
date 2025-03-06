from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from jose import jwt, JWTError

# * Load environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  
ALGORITHM = "HS256"

router = APIRouter(prefix="/user", tags=["User"])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
ouath2_bearer = OAuth2PasswordBearer(tokenUrl='token')

# * Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# * Authenticate User
def authenticateUser(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return False
    return user

# * Generate JWT Access Token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {
        'sub': username,
        'id': user_id,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

# * decode JWT Access Token
def get_current_user(token: Annotated[str, Depends(ouath2_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")

# * Request Model for Creating Users
class UserRequest(BaseModel):
    email: str = Field(max_length=50)
    username: str = Field(max_length=30)
    firstname: str = Field(max_length=15)
    lastname: str = Field(max_length=15)
    password: str = Field(min_length=8, max_length=72)  # ✅ Updated max_length=72
    is_active: bool
    role: str = Field(max_length=15)

# * Login and Get JWT Access Token
@router.post("/getAccessToken")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token(user.username, user.id, timedelta(minutes=45))
    return {"access_token": token, "token_type": "bearer"}

# * Create New User
@router.post("/createUser", status_code=status.HTTP_201_CREATED)
async def createUser(create_user: UserRequest, db: Session = Depends(get_db)):
    hashed_password = bcrypt_context.hash(create_user.password)  # ✅ Hash the password
    user_obj = Users(
        email=create_user.email,
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        password=hashed_password,  # ✅ Store hashed password
        is_active=create_user.is_active,
        role=create_user.role
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"message": "User created successfully"}

# * Fetch User by ID
@router.get("/fetchuserbyid/{id}", status_code=status.HTTP_200_OK)
async def fetchuserbyid(id: int = Path(gt=0), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="No user found")
