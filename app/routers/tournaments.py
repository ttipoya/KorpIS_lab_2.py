from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])

@router.post("/", response_model=schemas.TournamentRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.TournamentCreate, db: Session = Depends(get_db)):
    obj = models.Tournament(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.TournamentRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Tournament)).all()

@router.get("/{item_id}", response_model=schemas.TournamentRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Tournament, item_id)
    if not obj:
        raise HTTPException(404, "Tournament not found")
    return obj

@router.put("/{item_id}", response_model=schemas.TournamentRead)
def update_item(item_id: int, payload: schemas.TournamentCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Tournament, item_id)
    if not obj:
        raise HTTPException(404, "Tournament not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Tournament, item_id)
    if not obj:
        raise HTTPException(404, "Tournament not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

@router.get("/{tournament_id}/matches", response_model=list[schemas.MatchRead])
def tournament_matches(tournament_id: int, db: Session = Depends(get_db)):
    t = db.get(models.Tournament, tournament_id)
    if not t:
        raise HTTPException(404, "Tournament not found")
    return t.matches
