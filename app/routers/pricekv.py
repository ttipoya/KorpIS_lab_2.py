from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/pricekv", tags=["Pricekv"])

@router.post("/", response_model=schemas.PriceKVRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.PriceKVCreate, db: Session = Depends(get_db)):
    obj = models.PriceKV(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.PriceKVRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.PriceKV)).all()

@router.get("/{item_id}", response_model=schemas.PriceKVRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.PriceKV, item_id)
    if not obj:
        raise HTTPException(404, "PriceKV not found")
    return obj

@router.put("/{item_id}", response_model=schemas.PriceKVRead)
def update_item(item_id: int, payload: schemas.PriceKVCreate, db: Session = Depends(get_db)):
    obj = db.get(models.PriceKV, item_id)
    if not obj:
        raise HTTPException(404, "PriceKV not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.PriceKV, item_id)
    if not obj:
        raise HTTPException(404, "PriceKV not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

