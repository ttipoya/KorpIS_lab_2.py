from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/", response_model=schemas.StaffRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.StaffCreate, db: Session = Depends(get_db)):
    obj = models.Staff(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.StaffRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Staff)).all()

@router.get("/{item_id}", response_model=schemas.StaffRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Staff, item_id)
    if not obj:
        raise HTTPException(404, "Staff not found")
    return obj

@router.put("/{item_id}", response_model=schemas.StaffRead)
def update_item(item_id: int, payload: schemas.StaffCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Staff, item_id)
    if not obj:
        raise HTTPException(404, "Staff not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Staff, item_id)
    if not obj:
        raise HTTPException(404, "Staff not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

