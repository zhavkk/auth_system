from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from core.models import db_helper
from core.config import settings
import uvicorn
from sqlalchemy.orm import Session 
from core.schemas.user import UserSchema
from core.schemas.user import UserCreate
from core.models.db_helper import get_db
from core.models import User
from core.security import get_password_hash
from api import router as router_1
from api import admin_router as admin_router
from api import yandex_router,vk_router
from core.config import ApiPrefix
main_app = FastAPI()
api_prefix = ApiPrefix()

main_app.include_router(
    router_1,
    prefix=api_prefix.prefix + api_prefix.v1.prefix
    )
main_app.include_router(
    admin_router,
    prefix=api_prefix.prefix + api_prefix.v1.prefix
    )

# yandex и vk не добавляю префикс, т.к приложения уже зарегал на прошлый redirect_url   
main_app.include_router(
    yandex_router
    )
main_app.include_router(
    vk_router
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
