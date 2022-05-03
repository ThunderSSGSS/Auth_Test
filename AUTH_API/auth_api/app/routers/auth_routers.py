from fastapi import APIRouter, HTTPException, Depends
import uuid

from app import schemas
from app.dependencies import get_cache_token, get_db_user, get_cache_user_url
from app import warnings as war
######___INTERNAL___######
from app.internal.database import User_CRUD
from app.internal.cache import Cache_User_Token, Cache_User_URL
from app.internal.auth import (verify_password, create_tokens, create_access_token, 
    create_signup_url)
from app.internal.validators import EmailValidator, PasswordValidator



router = APIRouter()


#############___SIGNUP___#################
@router.post("/signup/", response_model=schemas.UserCreated)
async def signup(user: schemas.UserCreate, db: User_CRUD = Depends(get_db_user), 
    cache: Cache_User_URL = Depends(get_cache_user_url)):

    #Init of data validations
    email_validator = EmailValidator()
    pwd_validator = PasswordValidator()

    if not email_validator.is_valid(user.email):
        raise HTTPException(status_code=400, detail=war.invalid_email_msg())
    
    if not pwd_validator.is_valid(user.password):
        raise HTTPException(status_code=400, detail=war.invalid_password_msg())
    #End validations
    
    #verify if email exist
    if await db.email_exist(user.email):
        raise HTTPException(status_code=400, detail=war.exist_msg('Email'))

    user.id = uuid.uuid4()
    user_created = schemas.UserCreated(email=user.email,id=user.id)

    #create a user
    db.create_user(user)
    await create_signup_url({'id':str(user.id),'email':user.email}, cache)

    return user_created


#############___COMPLETE_SIGNUP___#################
@router.post("/complete_signup/{url_key}", response_model=schemas.UserCreated)
async def complete_signup(url_key: uuid.UUID, user_pwds: schemas.UserUpdatePassword, 
    db:User_CRUD=Depends(get_db_user), cache_url: Cache_User_URL = Depends(get_cache_user_url)):
    
    #Init of validations
    pwd_validator = PasswordValidator()
    if not pwd_validator.is_valid(user_pwds.password):
        raise HTTPException(status_code=400, detail=war.invalid_password_msg())  
    #End of validations

    #get the user infos from the cache, using url_key
    uncomplete_user_info = await cache_url.get(str(url_key))
    if uncomplete_user_info is None:
        raise HTTPException(status_code=400, detail=war.the_link_key_expired())
    
    uncomplete_user_info['id']=uuid.UUID(uncomplete_user_info['id'])

    #get the user from the database
    db_uncomplete_user = await db.get_user(uncomplete_user_info['id'])
    if db_uncomplete_user is None:
        raise HTTPException(status_code=404, detail=war.not_found_msg('User'))

    #check if the user completed the signup
    if db_uncomplete_user.is_complete:
        raise HTTPException(status_code=404, detail=war.not_found_msg('link'))

    #compare passwords
    if not verify_password(user_pwds.last_password, db_uncomplete_user.password):
        raise HTTPException(status_code=400, detail=war.incorrect_password_msg())

    #completing the user signup
    signup_schema = schemas.CompleteSignup(password=user_pwds.password)
    db.complete_signup(db_uncomplete_user.id, signup_schema)

    user_created = schemas.UserCreated(email=db_uncomplete_user.email, 
        id=db_uncomplete_user.id)
    
    #deleting the url_key
    await cache_url.delete(str(url_key))
    return user_created



##########___AUTHENTICATION___##########
@router.post("/authenticate/")
async def authenticate_user(user: schemas.UserAuth, db: User_CRUD = Depends(get_db_user),
		cache: Cache_User_Token = Depends(get_cache_token)):
    
    #Init of validations
    email_validator = EmailValidator()
    pwd_validator = PasswordValidator()

    if not email_validator.is_valid(user.email):
        raise HTTPException(status_code=400, detail=war.invalid_email_msg())
    
    if not pwd_validator.is_valid(user.password):
        raise HTTPException(status_code=400, detail=war.invalid_password_msg())
    #End validations

    db_user = await db.get_user_by_email(user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail= war.not_found_msg('Email'))

    #check if the user completed the signup and is active
    if not db_user.is_complete or not db_user.is_active:
        raise HTTPException(status_code=404, detail=war.not_found_msg('Email'))

    if not verify_password(user.password, db_user.password):
    	raise HTTPException(status_code=400, detail=war.incorrect_password_msg())

    return await create_tokens({'id':str(db_user.id),'is_staff':db_user.is_staff},cache)


@router.post("/refresh/")
async def refresh_token(data: schemas.Refresh, cache: Cache_User_Token = Depends(get_cache_token)):
    return await create_access_token(data.refresh,cache)