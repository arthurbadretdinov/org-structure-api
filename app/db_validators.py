from sqlalchemy.orm import Session

from app.exceptions import ErrorCodeException
from app.models import Department


def check_department_exists(db: Session, department_id: int | None) -> Department | None:
    if department_id is None:
        return
    
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise ErrorCodeException(404, "Department does not exist")
    
    return department


def check_not_self_parent(department_id: int, parent_id: int | None):
    if parent_id == department_id:
        raise ErrorCodeException(422, "Department cannot be parent to itself")
    
    
def check_no_cycle(
    db: Session, 
    department_id: int, 
    parent_id: int | None
):
    while parent_id is not None:
        if parent_id == department_id:
            raise ErrorCodeException(422, "Cycle detected in department hierarchy")
        
        parent_id = (
            db.query(Department.parent_id).filter(Department.id == parent_id).scalar()
        )

    
def check_unique_department_name(
    db: Session, 
    name: str, 
    parent_id: int | None = None,
    exclude_id: int | None = None
):
    department = db.query(Department).filter(Department.name == name)
    
    if parent_id is None:
        department = department.filter(Department.parent_id.is_(None))
    else:
        department = department.filter(Department.parent_id == parent_id)
    
    if exclude_id:
        department = department.filter(Department.id != exclude_id)
    
    department = department.first()
    if department:
        raise ErrorCodeException(409, "Department name already exists under this parent")