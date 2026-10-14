from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import schemas
from . import crud
from .database import SessionLocal
app = FastAPI()




#Dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/employee/", response_model=schemas.EmployeeOut) #resp model de type employeeout
async def create_user(employee:schemas.EmployeeCreate,db:Session=Depends(get_db)):
    db_employee=crud.get_by_email(db,email=employee.email)
    if employee.password!=employee.confirm_password:
        raise HTTPException(status_code=400,detail="Passwords must match")
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await crud.add(db=db,employee=employee)