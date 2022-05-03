from fastapi import FastAPI
#Database
from .internal.database import engine, Base
#Routers
from .routers import auth_routers


async def async_main():
	async with engine.begin() as session:
		await session.run_sync(Base.metadata.create_all)

app = FastAPI()
app.include_router(auth_routers.router)


@app.on_event("startup")
async def startup():
	await async_main()

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()