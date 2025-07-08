from pydantic import BaseModel
from datetime import datetime


class ComplaintCreate(BaseModel):
    text: str


class ComplaintResponse(BaseModel):
    id: int
    status: str
    sentiment: str
    text: str
    category: str
    country: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
