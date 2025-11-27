from sqlalchemy.orm import Session
from sqlalchemy import select

def get_all(db: Session, model):
    return db.scalars(select(model)).all()

def get_by_id(db: Session, model, id_):
    return db.get(model, id_)

def create(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, obj, data: dict):
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj):
    db.delete(obj)
    db.commit()
    return True
