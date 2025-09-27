from sqlmodel import Session, select
from db.models import RoomType, Room, Guest, Booking, RoomTypeCreate


def get_all_room_types(session: Session):
    return session.exec(select(RoomType)).all()

def get_room_type(session: Session, room_type_id: int):
    return session.get(RoomType, room_type_id)


def create_room_type(session: Session, room_type_data: RoomTypeCreate):
    room_type = RoomType.from_orm(room_type_data)
    session.add(room_type)
    session.commit()
    session.refresh(room_type)
    return room_type

def get_all_rooms(session: Session):
    return session.exec(select(Room)).all()

def get_room(session: Session, room_id: int):
    return session.get(Room, room_id)

def get_available_rooms(session: Session):
    return session.exec(select(Room).where(Room.status == "available")).all()

def create_room(session: Session, room: Room):
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

def get_all_guests(session: Session):
    return session.exec(select(Guest)).all()

def get_guest(session: Session, guest_id: int):
    return session.get(Guest, guest_id)

def create_guest(session: Session, guest: Guest):
    session.add(guest)
    session.commit()
    session.refresh(guest)
    return guest

def get_all_bookings(session: Session):
    return session.exec(select(Booking)).all()

def get_booking(session: Session, booking_id: int) -> Booking | None:
    statement = select(Booking).where(Booking.id == booking_id)
    return session.exec(statement).first()


def create_booking(session: Session, booking: Booking):
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking

def delete_booking(session: Session, booking: Booking):
    session.delete(booking)
    session.commit()
