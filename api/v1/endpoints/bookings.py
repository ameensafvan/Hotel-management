from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from db.database import get_session
from db.models import Booking, BookingCreate, BookingPublic, Room
from db.crud import get_all_bookings, get_booking, create_booking, delete_booking
from services.booking_service import book_room

router = APIRouter(tags=["Bookings"])

@router.get("/bookings", response_model=List[BookingPublic])
def read_bookings(session: Session = Depends(get_session)):
    return get_all_bookings(session)

@router.get("/bookings/{booking_id}", response_model=BookingPublic)
def read_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/bookings", response_model=BookingPublic)
def create_booking_endpoint(booking_data: BookingCreate, session: Session = Depends(get_session)):
    return book_room(
        session,
        guest_id=booking_data.guest_id,
        room_id=booking_data.room_id,
        check_in=booking_data.check_in_date,
        check_out=booking_data.check_out_date,
        total_amount=booking_data.total_amount
    )

@router.put("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = "canceled"
    room = session.get(Room, booking.room_id)
    if room:
        room.status = "available"
        session.add(room)

    session.add(booking)
    session.commit()
    return {"message": "Booking cancelled successfully"}

@router.delete("/bookings/{booking_id}")
def delete_booking_endpoint(booking_id: int, session: Session = Depends(get_session)):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    room = session.get(Room, booking.room_id)
    if room:
        room.status = "available"
        session.add(room)

    delete_booking(session, booking)
    return {"message": "Booking deleted successfully"}
