from pydantic import BaseModel,ConfigDict
from app.enums import Gender,ContractType,AccountStatus,RoleType
from datetime import date,datetime
from typing import List
class OurBaseModel(BaseModel):
    model_config=ConfigDict(from_attributes=True)

class EmployeeBase(OurBaseModel):
    first_name :str
    last_name:str
    email:str
    password:str |None=None
    number : str
    gender : Gender
    date_of_birth : date
    address : str |None=None
    cnss_number : str |None=None
    contract_type : ContractType
    roles:List[RoleType]
    phone_number:str|None=None

class EmployeeCreate(EmployeeBase):
    password:str|None=None #str | None (the type)
    #This says the value may be a string or None. Without it, Pydantic rejects None for a str field.
    #2. = None (the default)
    #This makes the field optional. If the client doesn’t send it, Pydantic fills in None. Without a default, the field is required.
    confirm_password:str|None=None
class EmployeeOut(EmployeeBase):
    id:int
    created_at:datetime