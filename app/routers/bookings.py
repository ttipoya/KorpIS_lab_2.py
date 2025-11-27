from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=schemas.BookingRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    if not db.get(models.Player, payload.player_id):
        raise HTTPException(400, 'Player not found')
    if not db.get(models.Room, payload.room_id):
        raise HTTPException(400, 'Room not found')
    overlapping = db.scalars(
        select(models.Booking).filter(
            models.Booking.room_id == payload.room_id,
            models.Booking.end_time > payload.start_time,
            models.Booking.start_time < payload.end_time,
            models.Booking.status != 'cancelled'
        )
    ).first()
    if overlapping:
        raise HTTPException(400, 'Room already booked for this time range')
    obj = models.Booking(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.BookingRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Booking)).all()

@router.get("/{item_id}", response_model=schemas.BookingRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Booking, item_id)
    if not obj:
        raise HTTPException(404, "Booking not found")
    return obj

@router.put("/{item_id}", response_model=schemas.BookingRead)
def update_item(item_id: int, payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Booking, item_id)
    if not obj:
        raise HTTPException(404, "Booking not found")
    overlapping = db.scalars(
        select(models.Booking).filter(
            models.Booking.room_id == payload.room_id,
            models.Booking.booking_id != item_id,
            models.Booking.end_time > payload.start_time,
            models.Booking.start_time < payload.end_time,
            models.Booking.status != 'cancelled'
        )
    ).first()
    if overlapping:
        raise HTTPException(400, 'Room already booked for this time range')
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Booking, item_id)
    if not obj:
        raise HTTPException(404, "Booking not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}
