from pydantic import BaseModel, EmailStr
from typing import Optional, List

class AuthHistoryBase(BaseModel):
    ip_address: Optional[str]
    user_agent: Optional[str]
    success: bool = True

class AuthHistoryCreate(AuthHistoryBase):
    pass

class AuthHistory(AuthHistoryBase):
    id: int
    login_time: str
    user_id: int

    class Config:
        from_attributes = True