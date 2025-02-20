from sqlalchemy.orm import Session  
from core.models.role import Role
from typing import Optional

def get_role_by_name(db: Session, role_name: str) -> Optional[Role]:
    query = db.query(Role).filter(Role.name == role_name)
    return query.first()

def create_role(db: Session, name: str, description: Optional[str] = None) -> Role:
    new_role = Role(name=name, description=description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
