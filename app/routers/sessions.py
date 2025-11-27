from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=schemas.GameSessionRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.GameSessionCreate, db: Session = Depends(get_db)):
    obj = models.GameSession(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.GameSessionRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.GameSession)).all()

@router.get("/{item_id}", response_model=schemas.GameSessionRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.GameSession, item_id)
    if not obj:
        raise HTTPException(404, "GameSession not found")
    return obj

@router.put("/{item_id}", response_model=schemas.GameSessionRead)
def update_item(item_id: int, payload: schemas.GameSessionCreate, db: Session = Depends(get_db)):
    obj = db.get(models.GameSession, item_id)
    if not obj:
        raise HTTPException(404, "GameSession not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.GameSession, item_id)
    if not obj:
        raise HTTPException(404, "GameSession not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

