from datetime import date

from sqlalchemy.orm import Session
from app.models import Department, Employee
from app.utils import validate_name
from app.db_validators import check_department_exists, check_unique_department_name

def create_department_service(
    db: Session, 
    name: str, 
    parent_id: int | None
) -> Department:
    name = validate_name(name, "Department name")
    check_department_exists(db, parent_id)
    check_unique_department_name(db, name, parent_id)
    
    db_department = Department(name=name, parent_id=parent_id)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    
    return db_department


def create_employee_service(
    db: Session,
    department_id: int,
    full_name: str,
    position: str,
    hired_at: date | None = None
) -> Employee:
    full_name = validate_name(full_name, "Employee full name")
    position = validate_name(position, "Employee position")
    check_department_exists(db, department_id)
    
    db_employee = Employee(
        department_id=department_id,
        full_name=full_name,
        position=position,
        hired_at=hired_at
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return db_employee