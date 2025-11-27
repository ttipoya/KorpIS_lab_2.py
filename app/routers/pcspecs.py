from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/pcspecs", tags=["Pcspecs"])

@router.post("/", response_model=schemas.PCSpecRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.PCSpecCreate, db: Session = Depends(get_db)):
    obj = models.PCSpec(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.PCSpecRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.PCSpec)).all()

@router.get("/{item_id}", response_model=schemas.PCSpecRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.PCSpec, item_id)
    if not obj:
        raise HTTPException(404, "PCSpec not found")
    return obj

@router.put("/{item_id}", response_model=schemas.PCSpecRead)
def update_item(item_id: int, payload: schemas.PCSpecCreate, db: Session = Depends(get_db)):
    obj = db.get(models.PCSpec, item_id)
    if not obj:
        raise HTTPException(404, "PCSpec not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.PCSpec, item_id)
    if not obj:
        raise HTTPException(404, "PCSpec not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

