from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/clubs", tags=["Clubs"])

@router.post("/", response_model=schemas.ClubRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.ClubCreate, db: Session = Depends(get_db)):
    obj = models.Club(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.ClubRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Club)).all()

@router.get("/{item_id}", response_model=schemas.ClubRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Club, item_id)
    if not obj:
        raise HTTPException(404, "Club not found")
    return obj

@router.put("/{item_id}", response_model=schemas.ClubRead)
def update_item(item_id: int, payload: schemas.ClubCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Club, item_id)
    if not obj:
        raise HTTPException(404, "Club not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Club, item_id)
    if not obj:
        raise HTTPException(404, "Club not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

@router.get("/{club_id}/arenas", response_model=list[schemas.ArenaRead])
def club_arenas(club_id: int, db: Session = Depends(get_db)):
    club = db.get(models.Club, club_id)
    if not club:
        raise HTTPException(404, "Club not found")
    return club.arenas

@router.get("/{club_id}/memberships", response_model=list[schemas.MembershipRead])
def club_memberships(club_id: int, db: Session = Depends(get_db)):
    club = db.get(models.Club, club_id)
    if not club:
        raise HTTPException(404, "Club not found")
    return club.memberships

@router.get("/{club_id}/tournaments", response_model=list[schemas.TournamentRead])
def club_tournaments(club_id: int, db: Session = Depends(get_db)):
    club = db.get(models.Club, club_id)
    if not club:
        raise HTTPException(404, "Club not found")
    return club.tournaments
