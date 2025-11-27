from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/configkv", tags=["Configkv"])

@router.post("/", response_model=schemas.ConfigKVRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.ConfigKVCreate, db: Session = Depends(get_db)):
    obj = models.ConfigKV(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.ConfigKVRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.ConfigKV)).all()

@router.get("/{item_id}", response_model=schemas.ConfigKVRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.ConfigKV, item_id)
    if not obj:
        raise HTTPException(404, "ConfigKV not found")
    return obj

@router.put("/{item_id}", response_model=schemas.ConfigKVRead)
def update_item(item_id: int, payload: schemas.ConfigKVCreate, db: Session = Depends(get_db)):
    obj = db.get(models.ConfigKV, item_id)
    if not obj:
        raise HTTPException(404, "ConfigKV not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.ConfigKV, item_id)
    if not obj:
        raise HTTPException(404, "ConfigKV not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

