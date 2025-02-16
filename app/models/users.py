from .base import Base

class User(Base):
    __tablename__ = "Users"
    username: str
    password: str
