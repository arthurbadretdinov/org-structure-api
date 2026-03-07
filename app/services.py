from datetime import date

from sqlalchemy.orm import Session, selectinload
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


def build_selectinload_options(max_depth: int, include_employees: bool):
    options = []

    if include_employees:
        options.append(selectinload(Department.employees))

    for depth in range(1, max_depth + 1):
        option = selectinload(Department.children)
        for _ in range(depth - 1):
            option = option.selectinload(Department.children)
        if include_employees:
            option = option.selectinload(Department.employees)
        options.append(option)

    return options


def build_tree(
    department: Department,
    depth: int,
    include_employees: bool
):
    result = {
        "department": {
            "id": department.id,
            "name": department.name,
            "parent_id": department.parent_id,
            "created_at": department.created_at
            },
        "children": []
    }
    
    if include_employees:
        result["employees"] = []
        for employee in department.employees:
            result["employees"].append(employee)

    if depth > 0:
        for child in department.children:
            result["children"].append(build_tree(child, depth - 1, include_employees))
         
    return result



def get_department_service(
    db: Session,
    department_id: int,
    depth: int = 1,
    include_employees: bool = True
):
    check_department_exists(db, department_id)
    
    options = build_selectinload_options(depth, include_employees)
    
    department = (
        db.query(Department)
        .options(*options)
        .filter(Department.id == department_id)
        .first()
    )
    
    response = build_tree(department, depth, include_employees)
    
    return response