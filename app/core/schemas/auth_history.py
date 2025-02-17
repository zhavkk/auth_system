from pydantic import BaseModel


class AuthHistorySchema(BaseModel):
    id: int
    user_id: int
    login_time: str
    user_agent: str
    ip_address: str
