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
import os
from core.config import settings
from core.kafka_producer import publish_registration_event
router = APIRouter(prefix="/login/yandex")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/yandex/token")

#TODO: TO .ENV
YANDEX_CLIENT_ID = settings.yandex_client_id
YANDEX_CLIENT_SECRET = settings.yandex_client_secret
REDIRECT_URI = settings.redirect_uri


@router.get("/")
def login_yandex():
    """
    перенаправляем на яндекс
    """
    yandex_oauth_url = (
        "https://oauth.yandex.ru/authorize?"
        "response_type=code"
        f"&client_id={YANDEX_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=login:email" 
    )
    return {"redirect_url": yandex_oauth_url}


@router.get("/callback")
def yandex_callback(code: str, db: Session = Depends(get_db)):
    """
    Яндекс перенаправляет на этот эндпоинт с параметром code,
    По этому коду мы запросим access_token от Яндекса и узнаем данные о пользователе.
    """
    token_url = "https://oauth.yandex.ru/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": YANDEX_CLIENT_ID,
        "client_secret": YANDEX_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not get token from Yandex")

    token_data = response.json()

    headers = {"Authorization": f"OAuth {token_data['access_token']}"}
    userinfo_resp = requests.get("https://login.yandex.ru/info?format=json", headers=headers)
    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not fetch user info from Yandex")

    userinfo = userinfo_resp.json()

    yandex_id = userinfo["id"]
    email = userinfo["default_email"]

    user = db.query(User).filter(User.yandex_id == yandex_id).first()
    if not user:
        user = User(
            username=email, 
            email=email,
            yandex_id=yandex_id,
            social_provider="yandex",
            role_id=2,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(
        data={"username": user.username, "role_id": user.role_id}
    )
    publish_registration_event(user)

    return {"access_token": access_token, "token_type": "bearer"}
