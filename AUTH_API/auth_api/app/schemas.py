#from typing import List, Optional
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

class UserPassword(BaseModel):
    password: str

class CompleteSignup(UserPassword):
    is_complete=True


##############_____Authenticate____######################
class UserAuth(UserCreate):
    pass

class Refresh(BaseModel):
    refresh: str

class UserUpdatePassword(BaseModel):
    last_password: str
    password: str