from datetime import date, datetime
from typing import List, Annotated
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

str200_type = Annotated[str, mapped_column(String(200), nullable=False)]
created_at_type = Annotated[
    datetime, 
    mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
]


class Department(Base):
    __tablename__ = "departments"
    __table_args__ = (
        UniqueConstraint('parent_id', 'name', name='uq_department_parent_name'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str200_type]
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), 
        nullable=True
    )
    created_at: Mapped[created_at_type]
    
    parent: Mapped["Department | None"] = relationship(
        back_populates="children",
        remote_side=[id]
    )
    children: Mapped[List["Department"]] = relationship(
        back_populates="parent",
        passive_deletes=True
    )
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan"
    )
    
class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), 
        nullable=False
    )
    full_name: Mapped[str200_type]
    position: Mapped[str200_type]
    hired_at: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[created_at_type]
    
    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )