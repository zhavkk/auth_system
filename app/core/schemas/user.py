from pydantic import BaseModel,EmailStr,Field

class UserCreate(BaseModel):
    



class UserSchema(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr
    password: str



