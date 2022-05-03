import uuid
import asyncio
from jose import jwt
from fastapi import HTTPException, Request
from passlib.context import CryptContext
from app.internal.cache import Cache_User_Token



#################___PASSWORD_HASH____############################
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password:str):
    return pwd_context.hash(password)



################___PERMISSIONS___###################################
async def _get_user_info_by_token(req: Request, cache: Cache_User_Token):
	if "Authorization" in req.headers:
		user_info = await cache.get_access(req.headers["Authorization"])
		if user_info is None:
			raise HTTPException(status_code=401,detail="Unauthorized")
		return user_info
	raise HTTPException(status_code=400, detail="Authentication not provited")

async def is_authenticated(req:Request, cache:Cache_User_Token):
	user_info = await _get_user_info_by_token(req,cache)
	return user_info['id']

async def has_admin_permission(req: Request, cache:Cache_User_Token):
	user_info = await _get_user_info_by_token(req,cache)
	if user_info['is_staff']:
   		return user_info['id']
	raise HTTPException(status_code=401,detail="Unauthorized")