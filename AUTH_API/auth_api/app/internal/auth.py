import uuid
import asyncio
from jose import jwt
from fastapi import HTTPException, Request
from passlib.context import CryptContext
from app.internal.cache import Cache_User_Token, Cache_User_URL
from app.settings import AUTH
####_CELERY_#####
from app.internal.celery import send_email




#################___PASSWORD_HASH____############################
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password:str):
    return pwd_context.hash(password)



#################___JWT___####################################
SECRET_KEY = AUTH['SECRET_KEY']
ALGORITHM = AUTH['ALGORITHM']

async def create_tokens(user_info:dict, cache: Cache_User_Token):
	"""
	Used to sign in (Create a new access and refresh token)
	user_info: is a dict that contain 'id' and 'is_staff'
	"""
	access = jwt.encode({'sub': str(uuid.uuid4())}, SECRET_KEY, algorithm=ALGORITHM)
	refresh = jwt.encode({'sub': str(uuid.uuid4())}, SECRET_KEY, algorithm=ALGORITHM)
	data = {'access':access,'refresh':refresh}
	await asyncio.gather(
		*[cache.set_access(access,user_info),
		cache.set_refresh(refresh,user_info)]
		)
	return data



async def create_access_token(refresh_token:str, cache: Cache_User_Token):
	"""
	Used to refresh (create a new access token)
	"""
	user_info = await cache.get_refresh(refresh_token)
	if user_info is None:
		raise HTTPException(status_code=403, detail="Forbidden, invalid refresh token")

	access = jwt.encode({'sub': str(uuid.uuid4())}, SECRET_KEY, algorithm=ALGORITHM)
	await cache.set_access(access,user_info)
	return {'access':access}


#################___URLS___####################################
def _signup_email_message(url_key: str):
	return "Click "+AUTH['COMPLETE_SIGNUP_LINK']+url_key+" to complete signup."


async def create_signup_url(uncomplete_user_info: dict, cache: Cache_User_URL):
	""" 
	This function creates a url key to signup the user, 
	and save it in cache
	uncomplete_user_info: is a dict that contain 'id' and 'email'
	"""
	key= str(uuid.uuid4())
	await cache.set(key, {'id':uncomplete_user_info['id']})
	send_email.delay(uncomplete_user_info['email'], "SIGNUP MESSAGE", _signup_email_message(key))



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