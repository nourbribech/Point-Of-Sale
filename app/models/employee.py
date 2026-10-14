from sqlalchemy import CheckConstraint, Column, Integer, String, Enum, DateTime, Date,func
from app.database import Base
from app.enums import ContractType, AccountStatus, Gender, RoleType
from sqlalchemy.orm import relationship
class Employee(Base): # Employee inherits Base
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    number = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    gender = Column(Enum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=True)
    cnss_number = Column(String, unique=True, nullable=True)
    contract_type = Column(Enum(ContractType), nullable=False)
    employee_roles = relationship(
    "EmployeeRole",
    back_populates="employee",
    cascade="all, delete-orphan",)
    
    account_status = Column(Enum(AccountStatus), default=AccountStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
     #default vs server_default: default is for Python-side defaults, while server_default is for database-side defaults. Using server_default ensures that the default value is set at the database level, which can be important for consistency and performance.

    __table_args__ = (
    CheckConstraint(
        r"contract_type IN ('CDI', 'CDD') "
        r"AND cnss_number IS NOT NULL "
        r"AND cnss_number ~ '^\d{8}-\d{2}$'",
        name="ck_employee_valid_cnss_number",
        ),
    )
    @property
    def roles(self):
        return [er.role_name for er in self.employee_roles]