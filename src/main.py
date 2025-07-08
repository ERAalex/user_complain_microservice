from fastapi import FastAPI
from .database import engine, Base
from src.complains.routes import router as complaints_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(complaints_router, prefix="/complaints", tags=["Complaints"])


# uvicorn src.main:app --reload
