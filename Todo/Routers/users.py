from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext

# * router to main.py for the API calling
router = APIRouter(prefix="/user", tags=["User"])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

# * Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class UserRequest(BaseModel):
    email : str = Field(max_length=50)
    username : str = Field(max_length=30)
    firstname : str = Field(max_length=15)
    lastname : str = Field(max_length=15)
    hashed_password : str = Field(max_length=16)
    is_active : bool
    role : str = Field(max_length=15)
    
@router.post("/createUser", status_code=status.HTTP_201_CREATED)
async def createUser(create_user: UserRequest, db: Session = Depends(get_db)):
    hash_password = bcrypt_context.hash(create_user.hashed_password)
    user_obj = Users(
        email=create_user.email,
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        hashed_password=hash_password,
        is_active=create_user.is_active,
        role=create_user.role
    )
    
    if(user_obj.is_active):
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)

    else:
        raise HTTPException(status_code=404, detail="user is not active")