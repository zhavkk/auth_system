from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_id: int = 2  # Default role is 'user'
    social_provider: Optional[str] = None  # yandex/vk/local

class UserSchema(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserSchema):
    password_hash: str

