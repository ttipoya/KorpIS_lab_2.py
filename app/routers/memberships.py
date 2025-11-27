from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/memberships", tags=["Memberships"])

@router.post("/", response_model=schemas.MembershipRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.MembershipCreate, db: Session = Depends(get_db)):
    obj = models.Membership(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.MembershipRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Membership)).all()

@router.get("/{item_id}", response_model=schemas.MembershipRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Membership, item_id)
    if not obj:
        raise HTTPException(404, "Membership not found")
    return obj

@router.put("/{item_id}", response_model=schemas.MembershipRead)
def update_item(item_id: int, payload: schemas.MembershipCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Membership, item_id)
    if not obj:
        raise HTTPException(404, "Membership not found")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Membership, item_id)
    if not obj:
        raise HTTPException(404, "Membership not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}

