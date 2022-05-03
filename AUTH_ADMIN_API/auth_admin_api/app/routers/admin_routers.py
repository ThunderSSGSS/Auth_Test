from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app import schemas
from app.dependencies import get_db_user, permission_admin
from app.internal.database import User_CRUD
from app import warnings as war
from app.internal.validators import EmailValidator, PasswordValidator
import uuid


router = APIRouter()


########_______________CREATE_____________#########
@router.post("/admin/users/", response_model=schemas.UserCreated)
async def create_user(user: schemas.UserAdminCreate, 
    db: User_CRUD = Depends(get_db_user), user_ids = Depends(permission_admin)):
    
    #Init of validations
    email_validator = EmailValidator()
    pwd_validator = PasswordValidator()

    if not email_validator.is_valid(user.email):
        raise HTTPException(status_code=400, detail=war.invalid_email_msg())
    
    if not pwd_validator.is_valid(user.password):
        raise HTTPException(status_code=400, detail=war.invalid_password_msg())
    #End validations

    #verify if the email exist
    if await db.email_exist(user.email):
        raise HTTPException(status_code=400, detail=war.exist_msg('Email'))
    
    #create user
    user.id = uuid.uuid4()
    db.admin_create_user(user)

    user_created = schemas.UserCreated(email=user.email, id=user.id)
    return user_created




########_______________READ_MANY_____________#########
@router.get("/admin/users/", response_model=List[schemas.UserAdmin])
async def read_users(skip: int = 0, limit: int = 100, db: User_CRUD = Depends(get_db_user), 
    user_ids = Depends(permission_admin)):

    users = await db.get_users(skip,limit)
    return users




########_______________READ_____________#########
@router.get("/admin/users/{user_id}", response_model=schemas.UserAdmin)
async def read_user(user_id: uuid.UUID, db: User_CRUD = Depends(get_db_user),
    user_ids = Depends(permission_admin)):

    db_user = await db.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=war.not_found_msg('User'))
    return db_user




########_______________UPDATE_____________#########
@router.put("/admin/users/{user_id}")
async def alter_user(user: schemas.UserAdminUpdate, user_id: uuid.UUID, 
    db: User_CRUD = Depends(get_db_user), user_ids = Depends(permission_admin)):
    
    #Init of validations
    email_validator = EmailValidator()
    if user.email is not None:
        if not email_validator.is_valid(user.email):
            raise HTTPException(status_code=400, detail=war.invalid_email_msg())
    #End validations

    db_user = await db.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=war.not_found_msg('User'))

    #verify if the email exist
    if user.email is not None:
        if await db.email_exist(user.email):
            raise HTTPException(status_code=400, detail=war.exist_msg('Email'))
    
    #update the user
    db.admin_update_user(db_user,user)
    return {'detail': war.altered_msg('User',id=str(user_id))}

    

########_______________DELETE_____________#########
@router.delete("/admin/users/{user_id}")
async def delete(user_id: uuid.UUID, db:User_CRUD = Depends(get_db_user), 
    user_ids=Depends(permission_admin)):

    db_user = await db.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=war.not_found_msg('User'))
        
    db.admin_delete_user(db_user.id)
    return {'detail': war.deleted_msg('User',id=str(user_id))}