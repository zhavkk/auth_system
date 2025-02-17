from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr
    password: str
    