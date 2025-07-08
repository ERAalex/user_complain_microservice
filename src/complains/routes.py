from fastapi import APIRouter, Depends, HTTPException, Request, Path
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from .schemas import ComplaintCreate, ComplaintResponse
from .models import Complaint
from src.database import get_db


router = APIRouter()


@router.post("/", response_model=ComplaintResponse)
def create_complaint(complaint_in: ComplaintCreate,
                     request: Request,
                     db: Session = Depends(get_db),):
    try:
        client_ip = request.client.host
        complaint = Complaint.create(db, complaint_in.text, client_ip)
        return complaint
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/close/{id}", response_model=ComplaintResponse)
def close_complaint(
    id: int = Path(..., description="ID complain to close"),
    db: Session = Depends(get_db),
):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    try:
        complaint.status = "closed"
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[ComplaintResponse])
def list_complaints(db: Session = Depends(get_db)):
    try:
        complaints = db.query(Complaint).all()
        return complaints
    except Exception as e:
        print(f"[DB Error] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recent", response_model=List[ComplaintResponse])
def list_recent_open_complaints(db: Session = Depends(get_db)):
    try:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        complaints = (
            db.query(Complaint)
            .filter(Complaint.status == "open")
            .filter(Complaint.timestamp >= one_hour_ago)
            .all()
        )
        return complaints
    except Exception as e:
        print(f"[DB Error] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
