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
import requests
from core.config import settings
import os
from core.kafka_producer import publish_registration_event
router = APIRouter(prefix="/login/vk",tags=["VK_AUTH"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/vk/token")
#TO .ENV
VK_REDIRECT_URI = settings.vk_redirect_uri
VK_CLIENT_SECRET = settings.vk_client_secret
VK_CLIENT_ID = settings.vk_client_id



@router.get("/")
def vk_login():
    """
    перенаправление на вк
    """
    vk_oauth_url = (
        "https://oauth.vk.com/authorize?"
        f"client_id={VK_CLIENT_ID}"
        "&display=page"
        "&response_type=code"
        f"&redirect_uri={VK_REDIRECT_URI}"
        "&scope=email"  
    )
    return {"redirect_url": vk_oauth_url}


@router.get("/callback")
def vk_callback(code: str, db: Session = Depends(get_db)):
    """
    VK перенаправляет на этот эндпоинт с параметром code,
    По этому коду мы запросим access_token от VK и узнаем данные о пользователе.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    token_url = "https://oauth.vk.com/access_token"
    params = {
        "client_id": VK_CLIENT_ID,
        "client_secret": VK_CLIENT_SECRET,
        "redirect_uri": VK_REDIRECT_URI,
        "code": code
    }
    resp = requests.get(token_url, params=params)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get token from VK")

    token_data = resp.json()


    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to get token from VK")

    access_token = token_data["access_token"]
    vk_id = str(token_data["user_id"])
    email = token_data.get("email")  
    db_user = db.query(User).filter(User.vk_id == vk_id).first()
    if not db_user:
        db_user = User(
            username=f"vk_{vk_id}", 
            email=email or f"vk_{vk_id}@example.com",  
            vk_id=vk_id,
            social_provider="vk",
            role_id=2
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    my_token = create_access_token(
        data={"username": db_user.username, "role_id": db_user.role_id}
    )
    
    publish_registration_event(db_user)

    return {
        "access_token": my_token,
        "token_type": "bearer"
    }