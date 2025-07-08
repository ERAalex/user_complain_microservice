from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from src.database import Base
from src.utils.external_services import ExternalServiceClient
from src.logger import logger


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
    def create(cls, db: Session, text: str, client_ip: str):
        try:
            external_services = ExternalServiceClient()
            category = external_services.categorize_complaint(text)
            country = external_services.detect_country_by_ip(client_ip)
            sentiment = external_services.analyze_sentiment(text)

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
        db.commit()
        db.refresh(complaint)
        return complaint
