from typing import Sequence
from sqlalchemy.orm import Session  
from core.models import AuthHistory
from fastapi import HTTPException

def get_all_auth_history(
    db: Session,
    current_user: User,
) -> Sequence[AuthHistory]:
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    stmt = db.query(AuthHistory).order_by(AuthHistory.id).all()  
    return stmt
