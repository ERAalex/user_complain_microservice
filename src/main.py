from fastapi import FastAPI
from src.database import engine, Base
from src.complains.routes import router as complaints_router
import asyncio

app = FastAPI()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_models()


app.include_router(complaints_router, prefix="/complaints", tags=["Complaints"])
