from typing import Optional#, List
from pydantic import BaseModel
from datetime import datetime
import uuid

#############____For_Normal___######################
class UserEmail(BaseModel):
    email: str

class UserCreate(UserEmail):
    password: str
    id:uuid.UUID=uuid.uuid4()

class UserCreated(UserEmail):
    id:uuid.UUID

class User(UserEmail):
    id: uuid.UUID
    created: datetime 

    class Config: #Its necessary to all schema that use database objects
        orm_mode = True

class UserUpdatePassword(BaseModel):
    last_password: str
    password: str

class UserPassword(BaseModel):
    password: str


#############____For_Admin___######################
class UserAdminCreate(UserCreate):
    is_staff: bool
    is_active: bool
    is_complete: bool = True

class UserAdminUpdate(BaseModel):
    is_staff: Optional[bool]
    is_active: Optional[bool]
    is_complete: Optional[bool]
    email: Optional[str]

class UserAdmin(User):
    is_staff: bool
    is_active: bool
    is_complete: bool
    password: str