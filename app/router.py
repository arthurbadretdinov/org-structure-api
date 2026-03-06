from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.db_validators import check_parent_exists, check_unique_department_name
from app.exceptions import ErrorCodeException
from app.models import Department as DbDepartment
from app.schemas import DepartmentCreate, Department
from app.services import create_department_service
from app.utils import validate_name

router = APIRouter(
    prefix="/departments"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/", response_model=Department)
def create_department(
    department: DepartmentCreate, 
    db: Session = Depends(get_db)
) -> DbDepartment:
    try:
        db_department = create_department_service(
            db, 
            department.name, 
            department.parent_id
        )
    except ErrorCodeException as e:
        raise HTTPException(
            status_code=e.code, 
            detail={"code": e.code, "message": e.message}
        )
    
    return db_department