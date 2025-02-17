
from pydantic import BaseModel
class RoleSchema(BaseModel):
    role: str = Field(max_length = 100)
    
