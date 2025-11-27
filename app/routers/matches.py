from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.post("/", response_model=schemas.MatchRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.MatchCreate, db: Session = Depends(get_db)):
    obj = models.Match(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.MatchRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Match)).all()

@router.get("/{item_id}", response_model=schemas.MatchRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Match, item_id)
    if not obj:
        raise HTTPException(404, "Match not found")
    return obj

@router.put("/{item_id}", response_model=schemas.MatchRead)
def update_item(item_id: int, payload: schemas.MatchCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Match, item_id)
    if not obj:
        raise HTTPException(404, "Match not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Match, item_id)
    if not obj:
        raise HTTPException(404, "Match not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

