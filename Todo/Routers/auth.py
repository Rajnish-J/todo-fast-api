from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from models import Users
from database import get_db

# * Load environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Authentication"])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/getAccessToken")

# * Authenticate User
def authenticate_user(username: str, password: str, db: Session):
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

# * Decode JWT Access Token
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

# * Login and Get JWT Access Token
@router.post("/getAccessToken")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token(user.username, user.id, timedelta(minutes=45))
    return {"access_token": token, "token_type": "bearer"}
