from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from db.database import get_session
from db.models import Guest, GuestCreate, GuestPublic
from db.crud import get_all_guests, get_guest, create_guest
from sqlalchemy.exc import IntegrityError


router = APIRouter(tags=["Guests"])

@router.get("/guests", response_model=List[GuestPublic])
def read_guests(session: Session = Depends(get_session)):
    """Get all guests"""
    return get_all_guests(session)

@router.post("/guests", response_model=GuestPublic)
def add_guest(guest_data: GuestCreate, session: Session = Depends(get_session)):
    guest = Guest(**guest_data.dict())
    try:
        return create_guest(session, guest)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Guest already exists with this email or phone")


@router.get("/guests/{guest_id}", response_model=GuestPublic)
def read_guest(guest_id: int, session: Session = Depends(get_session)):
    guest = get_guest(session, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest
