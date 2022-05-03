import aioredis
from fastapi import Request, Depends
from app.internal.database import SessionLocal, User_CRUD
from app.internal.cache import CACHE_URL, Cache_User_Token, Cache_User_URL
from app.internal.auth import has_admin_permission, is_authenticated


async def get_db_session():
	async with SessionLocal() as asession:
		async with asession.begin():
			yield asession

async def get_cache_session():
	redis =aioredis.Redis.from_url(CACHE_URL)
	async with redis.client() as asession:
		yield asession


#######__DATABASE__######

def get_db_user(asession=Depends(get_db_session)):
	return User_CRUD(asession)


######__CACHE__######

def get_cache_token(asession=Depends(get_cache_session)):
	return Cache_User_Token(asession)

def get_cache_user_url(asession=Depends(get_cache_session)):
	return Cache_User_URL(asession)


#######___PERMISSIONS___########

async def permission_admin(req: Request, cache:Cache_User_Token=Depends(get_cache_token)):
	return await has_admin_permission(req,cache)

async def permission_authenticated(req: Request, cache:Cache_User_Token=Depends(get_cache_token)):
	return await is_authenticated(req,cache)