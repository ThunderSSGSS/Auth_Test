from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#others
from app.settings import DATABASE as db
#Form model
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
#For crud
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.validators import EmailValidator


#################_____DATABASE____#############################
SQLALCHEMY_DATABASE_URL='postgresql://'+db['USER']+':'+db['PASSWORD']+'@'+db['LOCATION']+'/'+db['NAME']
engine = create_engine(#connect_args={"check_same_thread": False} is only for sqllite
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)

#The future session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()#Used to create database models


################____MODELS____#############################

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)#Hashed
    is_active = Column(Boolean, default=True)
    is_staff= Column(Boolean, default=True)#melhore
    is_complete= Column(Boolean, default=False) #if signup completed
    created = Column(DateTime, default=datetime.now())



#################____CRUD___#############################

class BaseEDIT():
    """
    ATTENTION, i considered that all the methods arguments of this class 
    was validated, so that, please VALIDATE THE DATA BEFORE USE THE FUNCTIONS
    """
    model_class=None

    def __init__(self, db:Session):
        self.db=db

    def create_object(self, object_schema:dict):
        db_object = self.model_class(**object_schema)
        self.db.add(db_object)
        self.db.commit()

    def update_object(self, object_id, new_data_schema:dict):
        self.db.query(self.model_class).filter(self.model_class.id == object_id).update(new_data_schema)
        self.db.commit()

    def delete_object(self, object_id):
        query = delete(self.model_class).where(self.model_class.id == object_id)
        self.db.execute(query)
        self.db.commit()

    def validate_create(self, data_dict:dict):
        return True

    def validate_update(self, data_dict:dict):
        return True



class User_EDIT(BaseEDIT):
    model_class=User

    def validate_create(self, data_dict:dict):
        email_validator = EmailValidator()
        return email_validator.is_valid(data_dict['email'])

    def validate_update(self, data_dict:dict):
        email_validator = EmailValidator()
        try:
            if data_dict['email'] is not None:
                return email_validator.is_valid(data_dict['email'])
        except:
            pass
        return True

    