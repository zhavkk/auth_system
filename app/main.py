from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,ConfigDict


class UserSchema(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr
    password: str
    model_config = ConfigDict(extra='forbid')


UserSchema()
app = FastAPI()

@app.get("/")
def root():
    return "hello world"