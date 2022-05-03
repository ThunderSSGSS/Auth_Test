from sqlalchemy.ext import asyncio as asyncio_ext
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
#from sqlalchemy import update, delete
#others
from app.settings import DATABASE as db
import asyncio
#For CRUD
from app import schemas
from app.internal.auth import hash_password
from pydantic import BaseModel
from app.internal.validators import is_altered
#CELERY
from app.internal.celery import create_object, update_object, delete_object
#Form model
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid


#################_____DATABASE____#############################
SQLALCHEMY_DATABASE_URL='postgresql+asyncpg://'+db['USER']+':'+db['PASSWORD']+'@'+db['LOCATION']+'/'+db['NAME']
engine = asyncio_ext.create_async_engine(SQLALCHEMY_DATABASE_URL)#, #future=True)

#The future session
SessionLocal = sessionmaker(engine, expire_on_commit=False, 
	class_=asyncio_ext.AsyncSession)

Base = declarative_base()#Used to create database models


################____MODELS____#############################

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)#Hashed
    is_active = Column(Boolean, default=True)
    is_staff= Column(Boolean, default=False)
    is_complete= Column(Boolean, default=False) #if signup completed
    created = Column(DateTime, default=datetime.now())



#################____CRUD___#############################

class BaseAsyncCRUD():
    """
    ATTENTION, i considered that all the arguments of this class 
    was validated, so that, please VALIDATE THE DATA BEFORE USE THE FUNCTIONS
    """
    model_class=None
    tablename=None

    def __init__(self, db:AsyncSession):
        self.db=db

    async def _get_object_by_id(self,object_id):
        result = await self.db.execute(select(self.model_class).where(self.model_class.id==object_id))
        return result.scalars().first()

    async def _get_objects(self, skip: int=0, limit: int = 100):#Alter the order_by
        query = select(self.model_class).offset(skip).limit(limit).order_by(self.model_class.created)
        result = await self.db.execute(query)
        return result.scalars().all()

    def _create_object(self, object_schema:BaseModel):
        #send create transaction message to the broker
        create_object.delay(self.tablename, object_schema.dict())

    def _update_object(self, object_id, new_data_schema:BaseModel):
        #send the update transaction message to the broker
        update_object.delay(self.tablename,object_id,new_data_schema.dict())

    def _delete_object(self, object_id):
        #send the delete transaction message to the broker
        delete_object.delay(self.tablename,object_id)

    

class User_CRUD(BaseAsyncCRUD):
    model_class=User
    tablename="users"

    #___CREATE__#

    def create_user(self, user: schemas.UserCreate):
        user.password = hash_password(user.password)
        self._create_object(user)

    def admin_create_user(self, user: schemas.UserAdminCreate):
        user.password = hash_password(user.password)
        self._create_object(user)


    #__READ__#

    async def get_users(self, skip: int = 0, limit: int = 100):
        return await self._get_objects(skip,limit)

    async def get_user(self, user_id: uuid.UUID):
        return await self._get_object_by_id(user_id)

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(self.model_class).where(self.model_class.email == email))
        return result.scalars().first()

    async def email_exist(self, email:str):
        result = await self.db.execute(select(User).where(User.email == email))
        if result.scalars().first() is not None:
            return True
        return False


    #__UPDATE__#

    def update_user_password(self, user_id: uuid.UUID, 
        user: schemas.UserPassword):
        user.password = hash_password(user.password)
        self._update_object(user_id, user)

    def admin_update_user(self, last_user: schemas.UserAdmin, 
        new_user: schemas.UserAdminUpdate):

        if is_altered(last_user,new_user):
            self._update_object(last_user.id,new_user)

    #__DELETE__#
            
    def admin_delete_user(self, user_id:uuid.UUID):
        self._delete_object(user_id)