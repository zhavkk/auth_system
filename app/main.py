from fastapi import FastAPI,status,Depends,HTTPException
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from core.models import db_helper
from core.config import settings
from contextlib import asynccontextmanager 
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from core.schemas.user import UserSchema
from core.schemas.user import UserCreate
from core.models.db_helper import get_db
from core.models import User

from core.security import get_password_hash
@asynccontextmanager
async def lifespan():
    yield

    await db_helper.dispose()


main_app = FastAPI(
)


@main_app.get("/hello/")
def root():
    return "hello world"

#@main_app.post("/users/create/")
@main_app.post("/register/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_dict = user_data.model_dump()
    password_hash = get_password_hash(user_dict.pop("password")) 
    user_dict["password_hash"] = password_hash

    new_user = User(**user_dict)

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

# # Получение информации о текущем пользователе
# @main_app.get("/me/", response_model=UserSchema)
# async def get_me(current_user: User = Depends(get_current_user)):
#     return current_user


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )