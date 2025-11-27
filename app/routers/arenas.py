from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/arenas", tags=["Arenas"])

@router.post("/", response_model=schemas.ArenaRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.ArenaCreate, db: Session = Depends(get_db)):
    obj = models.Arena(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.ArenaRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Arena)).all()

@router.get("/{item_id}", response_model=schemas.ArenaRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Arena, item_id)
    if not obj:
        raise HTTPException(404, "Arena not found")
    return obj

@router.put("/{item_id}", response_model=schemas.ArenaRead)
def update_item(item_id: int, payload: schemas.ArenaCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Arena, item_id)
    if not obj:
        raise HTTPException(404, "Arena not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Arena, item_id)
    if not obj:
        raise HTTPException(404, "Arena not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

@router.get("/{arena_id}/rooms", response_model=list[schemas.RoomRead])
def arena_rooms(arena_id: int, db: Session = Depends(get_db)):
    arena = db.get(models.Arena, arena_id)
    if not arena:
        raise HTTPException(404, "Arena not found")
    return arena.rooms
