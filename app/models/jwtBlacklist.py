from sqlalchemy import Column,Integer,String
from app.database import Base

class JWTBlacklist(Base):
    __tablename__="jwt_blacklist"

    id=Column(Integer,primary_key=True,nullable=False)
    token=Column(String,nullable=False)
    