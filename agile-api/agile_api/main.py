from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/values/", response_model=schemas.Value)
def create_value(value: schemas.ValueCreate, db: Session = Depends(get_db)):
    return crud.create_value(db=db, value=value)

@app.get("/values/", response_model=List[schemas.Value])
def read_values(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    values = crud.get_values(db, skip=skip, limit=limit)
    return values

@app.get("/values/{value_id}", response_model=schemas.Value)
def read_value(value_id: int, db: Session = Depends(get_db)):
    db_value = crud.get_value(db, value_id=value_id)
    if db_value is None:
        raise HTTPException(status_code=404, detail="Value not found")
    return db_value

@app.put("/values/{value_id}", response_model=schemas.Value)
def update_value(value: schemas.ValueCreate, value_id: int, db: Session = Depends(get_db)):
    db_value = crud.update_value(db, value_id=value_id, value=value)
    if db_value is None:
        raise HTTPException(status_code=404, detail="Value not found")
    return db_value

@app.delete("/values/{value_id}", response_model=schemas.Value)
def delete_value(value_id: int, db: Session = Depends(get_db)):
    db_value = crud.delete_value(db, value_id=value_id)
    if db_value is None:
        raise HTTPException(status_code=404, detail="Value not found")
    return db_value

@app.post("/principles/", response_model=schemas.Principle)
def create_principle(principle: schemas.PrincipleCreate, db: Session = Depends(get_db)):
    return crud.create_principle(db=db, principle=principle)

@app.get("/principles/", response_model=List[schemas.Principle])
def read_principles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    principles = crud.get_principles(db, skip=skip, limit=limit)
    return principles

@app.get("/principles/{principle_id}", response_model=schemas.Principle)
def read_principle(principle_id: int, db: Session = Depends(get_db)):
    db_principle = crud.get_principle(db, principle_id=principle_id)
    if db_principle is None:
        raise HTTPException(status_code=404, detail="Principle not found")
    return db_principle

@app.put("/principles/{principle_id}", response_model=schemas.Principle)
def update_principle(principle: schemas.PrincipleCreate, principle_id: int, db: Session = Depends(get_db)):
    db_principle = crud.update_principle(db, principle_id=principle_id, principle=principle)
    if db_principle is None:
        raise HTTPException(status_code=404, detail="Principle not found")
    return db_principle

@app.delete("/principles/{principle_id}", response_model=schemas.Principle)
def delete_principle(principle_id: int, db: Session = Depends(get_db)):
    db_principle = crud.delete_principle(db, principle_id=principle_id)
    if db_principle is None:
        raise HTTPException(status_code=404, detail="Principle not found")
    return db_principle