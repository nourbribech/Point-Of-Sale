from sqlalchemy.orm import Session
from . import models,schemas,emailUtil
from .models import EmployeeRole,AccountActivation
from .enums import TokenStatus
import uuid 
def get(db:Session, id:int):
    return db.query(models.Employee).filter(models.Employee.id==id).first()
    #<=> translated into an sql query

def get_by_email(db:Session,email:str):
    return db.query(models.Employee).filter(models.Employee.email==email).first()

def get_all(db:Session,skip:int=0,limit:int=100): #skip limit->pagination
    return db.query(models.Employee).offset(skip).limit(limit).all()

async def add(db:Session,employee:schemas.EmployeeCreate):
    #fixme later when reading about security
    employee.password=employee.password+"notreallyhashed" #fails if password is none!!!
    #fl moment hedha db_model andha id=null
    employee_data=employee.model_dump()

    employee_data.pop("confirm_password")#not in Employee model
    roles=employee_data.pop("roles")

    db_employee=models.Employee(**employee_data) # Employee(name="Sam", email="sam@x.com")
    db.add(db_employee)
    db.commit()#tsajel change fi db commit vs flush
    db.refresh(db_employee)#baad refresh db atat id ll employee ki naml refresh we get the id

    #add confirmation code
    token=str(uuid.uuid1())
    activation_code=models.AccountActivation(employee_id=db_employee.id,email=db_employee.email,status=TokenStatus.PENDING,token=token)
    db.add(activation_code)
    db.commit()
    link = f"http://127.0.0.1:8000/employee/activate?token={token}"
    for role in roles:#parcours indiv de chaque role car on a pas un champ roles ds la table Employee
        db_role=models.EmployeeRole(role_name=role,employee_id=db_employee.id)
        db.add(db_role)
    db.commit()
    await emailUtil.send_with_template(db_employee.email,{"first_name": db_employee.first_name,'link':link, 'code':activation_code.token})
    return db_employee #and let response_model=schemas.EmployeeOut in your route do the conversion. 
    #<=>return schemas.EmployeeOut.model_validate(db_employee) model_validate converts an orm object explicitly 

def get_confirmation_code(db:Session,code:str):
    return db.query(models.AccountActivation).filter(models.AccountActivation.token==code).first() #The function returns one AccountActivation object, or None if no row matches.
# SELECT * FROM account_activation
# WHERE token = :code
# LIMIT 1, then fetch it