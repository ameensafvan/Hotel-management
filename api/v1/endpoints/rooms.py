from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from db.database import get_session
from db.models import Room, RoomCreate, RoomPublic, RoomStatus, RoomType, RoomTypeCreate
from db.crud import create_room_type, get_all_room_types

router = APIRouter(tags=["Rooms"])


@router.post("/roomtypes", response_model=RoomType)
def add_room_type(data: RoomTypeCreate, session: Session = Depends(get_session)):
    """
    Create a new room type.
    """
    return create_room_type(session, data)

@router.get("/roomtypes", response_model=List[RoomType])
def list_room_types(session: Session = Depends(get_session)):
    """
    List all room types.
    """
    return get_all_room_types(session)


@router.get("/rooms", response_model=List[RoomPublic])
def read_rooms(session: Session = Depends(get_session)):
    """
    Get all rooms.
    """
    rooms = session.exec(select(Room)).all()
    return rooms

@router.get("/rooms/available", response_model=List[RoomPublic])
def read_available_rooms(session: Session = Depends(get_session)):
    """
    Get all rooms that are currently available.
    """
    rooms = session.exec(select(Room).where(Room.status == RoomStatus.available)).all()
    return rooms

@router.get("/rooms/{room_id}", response_model=RoomPublic)
def read_room(room_id: int, session: Session = Depends(get_session)):
    """
    Get a single room by its ID.
    """
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/rooms", response_model=RoomPublic)
def add_room(room_data: RoomCreate, session: Session = Depends(get_session)):
    """
    Create a new room, validating the room type and setting default status.
    """
    # Validate room_type_id exists
    if room_data.room_type_id is not None:
        room_type = session.get(RoomType, room_data.room_type_id)
        if not room_type:
            raise HTTPException(status_code=404, detail="Room type not found")
    
    room_dict = room_data.dict()
    room_dict["status"] = RoomStatus.available

    room = Room(**room_dict)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room
