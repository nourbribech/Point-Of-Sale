from sqlalchemy import Column,Integer,String,ForeignKey,Enum,DateTime, func
from app.database import Base
from app.enums import TokenStatus
from datetime import UTC, datetime

class AccountActivation(Base):
    __tablename__="account_activation"

    id=Column(Integer,primary_key=True,nullable=False)
    employee_id=Column(ForeignKey("employees.id"),nullable=False)
    token=Column(String,nullable=False)
    created_on=Column(DateTime, nullable=False,server_default=func.now())
    status=Column(Enum(TokenStatus),nullable=False)