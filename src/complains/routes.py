from fastapi import APIRouter, Depends, HTTPException, Request, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime, timedelta

from .schemas import ComplaintCreate, ComplaintResponse
from .models import Complaint
from src.database import get_db
from src.logger import logger

router = APIRouter()


@router.post("/", response_model=ComplaintResponse)
async def create_complaint(
    complaint_in: ComplaintCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    try:
        client_ip = request.client.host
        complaint = await Complaint.create(db, complaint_in.text, client_ip)

        logger.info(f"New complaint created {complaint.id}")
        return complaint
    except Exception as e:
        print(e)
        logger.error(f"Error on creation of complaint, error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/close/{id}", response_model=ComplaintResponse)
async def close_complaint(
    id: int = Path(..., description="ID complaint to close"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Complaint).filter(Complaint.id == id))
    complaint = result.scalars().first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    try:
        complaint.status = "closed"
        await db.commit()
        await db.refresh(complaint)
        logger.info(f"Complaint {complaint.id} closed")
        return complaint
    except Exception as e:
        await db.rollback()
        logger.error(f"Error on closing complaint {complaint.id}, error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[ComplaintResponse])
async def list_complaints(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Complaint))
        complaints = result.scalars().all()
        return complaints
    except Exception as e:
        logger.error(f"Error on getting complaints, error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recent", response_model=List[ComplaintResponse])
async def list_recent_open_complaints(db: AsyncSession = Depends(get_db)):
    try:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        stmt = (
            select(Complaint)
            .filter(Complaint.status == "open")
            .filter(Complaint.timestamp >= one_hour_ago)
        )
        result = await db.execute(stmt)
        complaints = result.scalars().all()
        return complaints
    except Exception as e:
        logger.error(f"Error on getting recent complaints, error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
