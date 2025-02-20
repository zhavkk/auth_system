from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from .roles import get_role_by_name
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.scalars().first()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    role_name: str) -> User:
    hashed_password = pwd_context.hash(password)
    
    query = select(Role).filter(Role.name == role_name)
    role = await db.execute(query)
    role = role.scalars().first()
    
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist.")
    
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role_id=role.id,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

