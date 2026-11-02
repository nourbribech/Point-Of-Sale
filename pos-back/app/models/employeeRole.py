from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, Date, func
from app.database import Base
from app.enums.role import RoleType
from sqlalchemy.orm import relationship

class EmployeeRole(Base):
    __tablename__ = "employee_roles"

    id = Column(Integer, primary_key=True, nullable=False)
    employee_id = Column(Integer,ForeignKey("employees.id"), nullable=False)
    role_name = Column(Enum(RoleType), nullable=False)
    employee = relationship(
        "Employee",
        back_populates="employee_roles",
    )
