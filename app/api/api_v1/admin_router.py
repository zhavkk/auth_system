from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.models.db_helper import get_db
from core.models.user import User
from core.models.auth_history import AuthHistory
from core.dependencies import get_admin_user

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return db.query(User).all()

@admin_router.get("/history")
def get_auth_history(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return db.query(AuthHistory).all()
