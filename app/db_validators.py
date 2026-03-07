from sqlalchemy.orm import Session

from app.exceptions import ErrorCodeException
from app.models import Department

def check_department_exists(db: Session, parent_id: int | None):
    if parent_id is None:
        return
    parent = db.query(Department).filter(Department.id == parent_id).first()
    if parent is None:
        raise ErrorCodeException(404, "Department does not exist")
    
def check_unique_department_name(db: Session, name: str, parent_id: int | None = None):
    department = db.query(Department).filter(Department.name == name)
    if parent_id is None:
        department = department.filter(Department.parent_id.is_(None))
    else:
        department = department.filter(Department.parent_id == parent_id)
    department = department.first()
    if department:
        raise ErrorCodeException(409, "Department name already exists under this parent")