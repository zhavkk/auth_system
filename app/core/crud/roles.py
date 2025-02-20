from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import Optional
from core.models.role import Role
async def get_role_by_name(db: AsyncSession, role_name: str) -> Optional["Role"]:
    query = select(Role).filter(Role.name == role_name)
    result = await db.execute(query)
    return result.scalars().first()

async def create_role(db: AsyncSession, name: str, description: Optional[str] = None) -> Role:
    new_role = Role(name=name, description=description)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role
