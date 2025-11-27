from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=schemas.RoomRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.RoomCreate, db: Session = Depends(get_db)):
    obj = models.Room(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.RoomRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Room)).all()

@router.get("/{item_id}", response_model=schemas.RoomRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Room, item_id)
    if not obj:
        raise HTTPException(404, "Room not found")
    return obj

@router.put("/{item_id}", response_model=schemas.RoomRead)
def update_item(item_id: int, payload: schemas.RoomCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Room, item_id)
    if not obj:
        raise HTTPException(404, "Room not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Room, item_id)
    if not obj:
        raise HTTPException(404, "Room not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

@router.get("/{room_id}/stations", response_model=list[schemas.StationRead])
def room_stations(room_id: int, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if not room:
        raise HTTPException(404, "Room not found")
    return room.stations

@router.get("/{room_id}/bookings", response_model=list[schemas.BookingRead])
def room_bookings(room_id: int, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if not room:
        raise HTTPException(404, "Room not found")
    return room.bookings

@router.get("/{room_id}/sessions", response_model=list[schemas.GameSessionRead])
def room_sessions(room_id: int, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if not room:
        raise HTTPException(404, "Room not found")
    return room.game_sessions
