# main.py
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

main_app = FastAPI()

main_app.include_router(router_1)

@main_app.get("/hello/")
def root():
    return "hello world"

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
