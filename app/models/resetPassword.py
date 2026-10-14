from sqlalchemy import Column,Integer,String,Enum,ForeignKey,DateTime, func
from app.database import Base
from app.enums import TokenStatus 
from datetime import UTC, datetime

class ResetPassword(Base):
    __tablename__="reset_password"

    id=Column(Integer,primary_key=True, nullable=False)
    employee_id=Column(Integer,ForeignKey("employees.id"),nullable=False)
    token=Column(String,nullable=False)
    expired_on=Column(DateTime, nullable=False,server_default=func.now())
    status=Column(Enum(TokenStatus),nullable=False)