from datetime import date, datetime

from pydantic import BaseModel


class Department(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    created_at: datetime
    
    class Config: 
        from_attributes = True
    

class Employee(BaseModel):
    id: int
    department_id: int
    full_name: str
    position: str
    hired_at: date | None = None
    created_at: datetime
    
    class Config: 
        from_attributes = True
    

class DepartmentCreate(BaseModel):
    name: str
    parent_id: int | None = None
   
 
class EmployeeCreate(BaseModel):
    full_name: str
    position: str
    hired_at: date | None = None
    
    
class DepartmentResponse(BaseModel):
    department: Department
    employees: list[Employee] | None = None
    children: list["DepartmentResponse"] = []

    class Config:
        from_attributes = True

DepartmentResponse.model_rebuild()
    
    
class DepartmentPatch(BaseModel):
    name: str | None = None
    parent_id: int | None = None