from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

# Enum for room status
class RoomStatus(str, Enum):
    available = "available"
    occupied = "occupied"
    booked = "booked"
    cancelled = "cancelled"

# Tables
class RoomTypeBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    base_rate: float

class RoomBase(SQLModel):
    room_number: str = Field(index=True)
    status: RoomStatus = Field(default=RoomStatus.available)
    room_type_id: Optional[int] = Field(default=None, foreign_key="roomtype.id")

class GuestBase(SQLModel):
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    phone_number: str

class BookingBase(SQLModel):
    check_in_date: date
    check_out_date: date
    total_amount: float
    status: str = "confirmed"

# Table models
class RoomType(RoomTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rooms: List["Room"] = Relationship(back_populates="room_type")

class Room(RoomBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room_type: Optional[RoomType] = Relationship(back_populates="rooms")
    bookings: List["Booking"] = Relationship(back_populates="room")

class Guest(GuestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bookings: List["Booking"] = Relationship(back_populates="guest")

class Booking(BookingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    guest_id: int = Field(foreign_key="guest.id")
    room_id: int = Field(foreign_key="room.id")
    guest: Guest = Relationship(back_populates="bookings")
    room: Room = Relationship(back_populates="bookings")

# Pydantic models for input/output
class RoomTypeCreate(RoomTypeBase):
    pass

class RoomCreate(RoomBase):
    pass

class GuestCreate(GuestBase):
    pass

class BookingCreate(BookingBase):
    guest_id: int
    room_id: int

class RoomPublic(RoomBase):
    id: int
    room_type: Optional[RoomTypeBase] = None

class GuestPublic(GuestBase):
    id: int

class BookingPublic(BookingBase):
    id: int
    guest_id: int
    room_id: int
    guest: GuestPublic
    room: RoomPublic
