from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import schemas
from . import crud, enums,models
from .database import SessionLocal
import datetime
from zoneinfo import ZoneInfo

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

@app.patch("/employee",response_model=schemas.BaseOut)
def confirm_account(confirmAccountInput:schemas.ConfirmAccount,db:Session=Depends(get_db)):
    confirmation_code=crud.get_confirmation_code(db,confirmAccountInput.confirmation_code)

    if not confirmation_code:
        raise HTTPException(status_code=400,detail="token does not exist")
    if confirmation_code.status==enums.TokenStatus.USED:
        raise HTTPException(status_code=400,detail="token already used")
    diff=datetime.datetime.now()-confirmation_code.created_on #en secondes
    now = datetime.datetime.now(ZoneInfo("Africa/Casablanca")).replace(tzinfo=None)
    diff = now - confirmation_code.created_on

    if diff > datetime.timedelta(hours=1):
        raise HTTPException(status_code=400, detail="token expired")

    db.query(models.Employee).filter(models.Employee.id==confirmation_code.employee_id).\
        update({models.Employee.account_status: enums.AccountStatus.ACTIVE}, synchronize_session=False)

    db.commit()

    db.query(models.AccountActivation).filter(models.AccountActivation.id==confirmation_code.id).\
            update({models.AccountActivation.status: enums.TokenStatus.USED}, synchronize_session=False)

    db.commit()
    return schemas.BaseOut(detail="confirmed",status_code=status.HTTP_200_OK)

options=[
    schemas.MatchyOption("First Name", "first_name",True,enums.FieldType.string),
    schemas.MatchyOption("Last Name", "last_name",True,enums.FieldType.string),
    schemas.MatchyOption("Email", "email",True,enums.FieldType.string,[schemas.MatchyCondition(enums.ConditionProperty.regex,enums.Comparer.e,"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")]),
    schemas.MatchyOption("Password", "password",True,enums.FieldType.string),
    schemas.MatchyOption("Number", "number",True,enums.FieldType.integer),
    schemas.MatchyOption("Date of Birth", "date_of_birth",True,enums.FieldType.string),
    schemas.MatchyOption("Adress", "adress",False,enums.FieldType.string),
    schemas.MatchyOption("Cnss Number", "cnss_number",True,enums.FieldType.string),
    schemas.MatchyOption("Contract Type", "contract_type",True,enums.FieldType.string,[schemas.MatchyCondition]),
]

@app.post("/employees/import")
def importEmployees():
    pass