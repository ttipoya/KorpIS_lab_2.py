from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/players", tags=["Players"])

@router.post("/", response_model=schemas.PlayerRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.PlayerCreate, db: Session = Depends(get_db)):
    obj = models.Player(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.PlayerRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Player)).all()

@router.get("/{item_id}", response_model=schemas.PlayerRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Player, item_id)
    if not obj:
        raise HTTPException(404, "Player not found")
    return obj

@router.put("/{item_id}", response_model=schemas.PlayerRead)
def update_item(item_id: int, payload: schemas.PlayerCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Player, item_id)
    if not obj:
        raise HTTPException(404, "Player not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Player, item_id)
    if not obj:
        raise HTTPException(404, "Player not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

@router.get("/{player_id}/memberships", response_model=list[schemas.MembershipRead])
def player_memberships(player_id: int, db: Session = Depends(get_db)):
    player = db.get(models.Player, player_id)
    if not player:
        raise HTTPException(404, "Player not found")
    return player.memberships

@router.get("/{player_id}/sessions", response_model=list[schemas.GameSessionRead])
def player_sessions(player_id: int, db: Session = Depends(get_db)):
    player = db.get(models.Player, player_id)
    if not player:
        raise HTTPException(404, "Player not found")
    return player.hosted_sessions

@router.get("/{player_id}/bookings", response_model=list[schemas.BookingRead])
def player_bookings(player_id: int, db: Session = Depends(get_db)):
    player = db.get(models.Player, player_id)
    if not player:
        raise HTTPException(404, "Player not found")
    return player.bookings

@router.get("/{player_id}/matches_won", response_model=list[schemas.MatchRead])
def player_matches(player_id: int, db: Session = Depends(get_db)):
    player = db.get(models.Player, player_id)
    if not player:
        raise HTTPException(404, "Player not found")
    return player.matches_won
