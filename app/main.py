from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from app.models import db_helper


@asynccontextmanager
async def lifespan():
    yield

    await db_helper.dispose()


UserSchema()
main_app = FastAPI(
    lifespan=lifespan
)


@main_app.get("/")
def root():
    return "hello world"