from fastapi import FastAPI
#Database
from .internal.database import engine, Base
#Routers
from .routers import admin_routers


async def async_main():
	async with engine.begin() as session:
		await session.run_sync(Base.metadata.create_all)

app = FastAPI()
app.include_router(admin_routers.router)