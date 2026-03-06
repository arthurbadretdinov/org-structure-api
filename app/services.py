from sqlalchemy.orm import Session
from app.models import Department
from app.utils import validate_name
from app.db_validators import check_parent_exists, check_unique_department_name

def create_department_service(
    db: Session, 
    name: str, 
    parent_id: int | None
) -> Department:
    name = validate_name(name)
    check_parent_exists(db, parent_id)
    check_unique_department_name(db, name, parent_id)
    
    db_department = Department(name=name, parent_id=parent_id)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    
    return db_department