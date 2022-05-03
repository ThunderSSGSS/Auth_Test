import json
from datetime import timedelta
from app.settings import CACHE as ch

CACHE_URL = 'redis://'+ch['LOCATION']
PREFIX = ch['PREFIX']

###################___CACHE_CLASSES___######################
class BaseAsyncCache():
	element_prefix=None
	element_expire=None

	def __init__(self, session, prefix=PREFIX):
		self.redis=session
		self.prefix=prefix

	def add_prefix(self, key:str):
		return self.prefix+':'+self.element_prefix+':'+key

	async def set(self, key:str, value):
		"""
		value: must be a object that json can serialize
		"""
		keyP = self.add_prefix(key)
		await self.redis.setex(keyP,timedelta(seconds=self.element_expire),
			value=json.dumps(value))

	def serializer_result(self, result:str):
		if result is not None:
			return json.loads(result)
		return result

	async def get(self, key:str):
		keyP = self.add_prefix(key)
		return self.serializer_result(await self.redis.get(keyP))

	async def delete(self, key:str):
		keyP = self.add_prefix(key)
		await self.redis.delete(keyP)




############___CACHE_AUTH_TOKENS__##################
class Cache_User_Token():
	def __init__(self, session, prefix=PREFIX):
		self.redis = session
		self.prefix = prefix
		self.access_prefix='access'
		self.refresh_prefix='refresh'

		self.access_expire=300
		self.refresh_expire=3600

	def add_prefix_access(self, key:str):
		return self.prefix+':'+self.access_prefix+':'+key

	def add_prefix_refresh(self, key:str):
		return self.prefix+':'+self.refresh_prefix+':'+key

	###########SET
	async def set_access(self, key:str, value:dict):
		keyP = self.add_prefix_access(key)
		await self.redis.setex(keyP,timedelta(seconds=self.access_expire),
			value=json.dumps(value))#.set(key,value,)

	async def set_refresh(self, key:str, value:dict):
		keyP = self.add_prefix_refresh(key)
		await self.redis.setex(keyP,timedelta(seconds=self.refresh_expire),
			value=json.dumps(value))#.set(key,value,)

	###########GET
	def serializer_result(self, result:str):
		if result is not None:
			return json.loads(result)
		return result

	async def get_access(self, key:str):
		keyP = self.add_prefix_access(key)
		return self.serializer_result(await self.redis.get(keyP))

	async def get_refresh(self, key:str):
		keyP = self.add_prefix_refresh(key)
		return self.serializer_result(await self.redis.get(keyP))



################___CACHE_URL_KEYS___#########################
class Cache_URL_Key(BaseAsyncCache):
	element_prefix='url'
	element_expire=300