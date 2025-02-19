from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AuthHistory
#from core.schemas.auth_history import AuthHistoryCreate


async def get_all_auth_history(
    session: AsyncSession,
    current_user: User,
) -> Sequence[AuthHistory]:
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    stmt = select(AuthHistory).order_by(AuthHistory.id)
    result = await session.scalars(stmt)
    return result.all()