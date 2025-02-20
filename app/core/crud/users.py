from sqlalchemy.orm import Session 
from passlib.context import CryptContext
from core.models.user import User
from core.models.role import Role
from typing import Optional
from core.security import get_password_hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    role_id: int,
    yandex_id: Optional[str] = None,
    vk_id: Optional[str] = None,
    social_provider: Optional[str] = None
) -> User:

    hashed_password = get_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role_id=role_id,  
        yandex_id=yandex_id,
        vk_id=vk_id,
        social_provider=social_provider,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
