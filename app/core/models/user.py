from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base
from pydantic import BaseModel
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    yandex_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    vk_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="SET DEFAULT"), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    social_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)  # yandex/vk/local

    role: Mapped["Role"] = relationship(back_populates="users")
    auth_history: Mapped[list["AuthHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str