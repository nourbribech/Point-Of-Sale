from sqlalchemy import create_engine #sqlalchemy as orm 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# 1. Create the engine that manages connections to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. Create the SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#When you inherit from this Base class, SQLAlchemy automatically maps your Python classes to database tables and manages their schemas.
Base = declarative_base() 
