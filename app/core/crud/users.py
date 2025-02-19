from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError


async def get_all_users(
    session: AsyncSession,
    current_user: User,
) -> Sequence[User]:
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)



async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user_dict = user_create.model_dump()
    password_hash = get_password_hash(user_dict.pop("password"))
    user = User(**user_dict, password_hash=password_hash)
    
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")