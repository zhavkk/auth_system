from pydantic import BaseModel, EmailStr
from typing import Optional, List



class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_id: int = 2  # Default role is 'user'
    social_provider: Optional[str] = None  # yandex/vk/local

class User(UserBase):
    id: int
    role: Role
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True

class UserInDB(User):
    password_hash: str

