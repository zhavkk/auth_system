from .base import Base
from sqlalchemy.orm import mapped_column
class User(Base):
    __tablename__ = "Users"
    username: Mapped[str] = mapped_column(unique=True)
    password: str