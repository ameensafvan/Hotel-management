from fastapi import FastAPI
from db.database import create_tables
from api.v1.endpoints import guests, rooms, bookings

app = FastAPI(title="Hotel Management API")

@app.on_event("startup")
def startup_event():
    create_tables()

app.include_router(guests.router)
app.include_router(rooms.router)
app.include_router(bookings.router)


