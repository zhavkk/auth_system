from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from core.models import db_helper
from core.config import settings
from contextlib import asynccontextmanager 
import uvicorn

@asynccontextmanager
async def lifespan():
    yield

    await db_helper.dispose()


main_app = FastAPI(
)


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