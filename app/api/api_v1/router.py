from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  
from core.crud import create_user, get_user_by_username
from core.models.user import User
from core.schemas.user import UserSchema, UserCreate
from core.models.db_helper import get_db
from core.models.user import Token
from core.security import create_access_token  
from typing import Any
from datetime import timedelta
from passlib.context import CryptContext
from core.security import verify_password
from core.models.auth_history import AuthHistory
router = APIRouter(prefix="/demo-auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/demo-auth/token")

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    user = create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        role_id=user_data.role_id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        social_provider=user_data.social_provider
    )

    return user

@router.post("/token", response_model=Token)
def login_for_access_token(
    request: Request,  # ip, user_agent
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_username(db, form_data.username)
    success = False

    if user and verify_password(form_data.password, user.password_hash):
        success = True
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"username": user.username, "role_id": user.role_id},
            expires_delta=access_token_expires
        )
        token_dict = {"access_token": access_token, "token_type": "bearer"}
    else:
        token_dict = {}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth_record = AuthHistory(
        user_id=user.id if user else None, 
        success=success,
        ip_address=request.client.host,     
        user_agent=request.headers.get("User-Agent"),  
    )
    db.add(auth_record)
    db.commit()

    return token_dict
#TODO: get_all_users for admin (nujno dostat' user_id from payload)

