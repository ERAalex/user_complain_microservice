from src.database import Base
from src.utils.external_services import ExternalServiceClient
from src.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(String, default="open")
    timestamp = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String, default="unknown")
    category = Column(String, default="")
    country = Column(String, default="")

    @classmethod
    async def create(cls, db: AsyncSession, text: str, client_ip: str):
        try:
            external_services = ExternalServiceClient()
            category = await external_services.categorize_complaint(text)  # если async
            country = await external_services.detect_country_by_ip(client_ip)  # если async
            sentiment = await external_services.analyze_sentiment(text)  # если async
        except Exception as e:
            logger.info(f"Error on create complain: error {e}")
            sentiment = "unknown"
            country = "unknown"
            category = "unknown"

        complaint = cls(
            text=text,
            sentiment=sentiment,
            country=country,
            category=category,
            status="open",
        )
        db.add(complaint)
        await db.commit()
        await db.refresh(complaint)
        return complaint
