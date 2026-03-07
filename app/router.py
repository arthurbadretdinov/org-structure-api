from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.exceptions import ErrorCodeException
from app.models import Department as DbDepartment, Employee as DbEmployee
from app.schemas import DepartmentCreate, Department, Employee, EmployeeCreate
from app.services import create_department_service, create_employee_service

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


@router.post("/{department_id}/employees", response_model=Employee)
def create_employee(
    department_id : int,
    employee: EmployeeCreate, 
    db: Session = Depends(get_db)
) -> DbEmployee:
    try:
        db_employee = create_employee_service(
            db, 
            department_id,
            employee.full_name, 
            employee.position, 
            employee.hired_at
        )
    except ErrorCodeException as e:
        raise HTTPException(
            status_code=e.code, 
            detail={"code": e.code, "message": e.message}
        )
    
    return db_employee