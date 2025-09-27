from sqlmodel import Session
from fastapi import HTTPException
from db.models import Booking, Guest, Room
from datetime import date

def book_room(session: Session, guest_id: int, room_id: int, check_in: date, check_out: date, total_amount: float) -> Booking:
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    room = session.get(Room, room_id)
    if not room or room.status != "available":
        raise HTTPException(status_code=400, detail="Room not available")

    nights = (check_out - check_in).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in")

    booking = Booking(
        guest_id=guest_id,
        room_id=room_id,
        check_in_date=check_in,
        check_out_date=check_out,
        total_amount=total_amount,
        status="confirmed"
    )

    # Update room status
    room.status = "occupied"

    session.add_all([booking, room])
    session.commit()
    session.refresh(booking)
    return booking
