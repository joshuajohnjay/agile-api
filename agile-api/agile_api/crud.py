from sqlalchemy.orm import Session

try:
    from . import models, schemas
except ImportError:
    import models, schemas

def get_value(db: Session, value_id: int):
    return db.query(models.Value).filter(models.Value.id == value_id).first()

def get_values(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Value).offset(skip).limit(limit).all()

def create_value(db: Session, value: schemas.ValueCreate):
    db_value = models.Value(title=value.title, description=value.description)
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return db_value

def update_value(db: Session, value_id: int, value: schemas.ValueCreate):
    db_value = db.query(models.Value).filter(models.Value.id == value_id).first()
    if db_value is not None:
        db_value.title = value.title
        db_value.description = value.description
        db.commit()
        db.refresh(db_value)
        return db_value

def delete_value(db: Session, value_id: int):
    db_value = db.query(models.Value).filter(models.Value.id == value_id).first()
    if db_value is not None:
        db.delete(db_value)
        db.commit()
        return db_value

def get_principle(db: Session, principle_id: int):
    return db.query(models.Principle).filter(models.Principle.id == principle_id).first()

def get_principles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Principle).offset(skip).limit(limit).all()

def create_principle(db: Session, principle: schemas.PrincipleCreate):
    db_principle = models.Principle(title=principle.title, description=principle.description)
    db.add(db_principle)
    db.commit()
    db.refresh(db_principle)
    return db_principle

def update_principle(db: Session, principle_id: int, principle: schemas.PrincipleCreate):
    db_principle = db.query(models.Principle).filter(models.Principle.id == principle_id).first()
    if db_principle is not None:
        db_principle.title = principle.title
        db_principle.description = principle.description
        db.commit()
        db.refresh(db_principle)
        return db_principle

def delete_principle(db: Session, principle_id: int):
    db_principle = db.query(models.Principle).filter(models.Principle.id == principle_id).first()
    if db_principle is not None:
        db.delete(db_principle)
        db.commit()
        return db_principle