from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.exceptions import ErrorCodeException
from app.schemas import (
    DepartmentCreate, 
    Department,
    DepartmentPatch, 
    DepartmentResponse, 
    Employee, 
    EmployeeCreate
)
from app.services import (
    create_department_service, 
    create_employee_service, 
    get_department_service,
    patch_department_service
)

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
) -> Department:
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
) -> Employee:
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


@router.get(
    "/{department_id}", 
    response_model=DepartmentResponse,
    response_model_exclude_none=True
)
def get_department(
    department_id: int, 
    depth: int = Query(1, ge=1, le=5),
    include_employees: bool = True,
    db: Session = Depends(get_db)
) -> DepartmentResponse:
    try:
        response = get_department_service(
            db, 
            department_id,
            depth,
            include_employees
        )
    except ErrorCodeException as e:
        raise HTTPException(
            status_code=e.code, 
            detail={"code": e.code, "message": e.message}
        )
    
    return DepartmentResponse.model_validate(response)


@router.patch("/{department_id}", response_model=Department)
def patch_department(
    department_id: int, 
    department: DepartmentPatch,
    db: Session = Depends(get_db)
) -> Department:
    try:
        db_department = patch_department_service(
            db, 
            department_id,
            department.name,
            department.parent_id
        )
    except ErrorCodeException as e:
        raise HTTPException(
            status_code=e.code, 
            detail={"code": e.code, "message": e.message}
        )
    
    return db_department