from typing import List
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from sqlalchemy.orm import Session

try:
    from . import crud, models, schemas
    from agile_api.database import SessionLocal, engine
except ImportError:
    import crud, models, schemas
    from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

SECRET_KEY = "9d86100bb6719b26e286af2eaa35a11f68878cb85f88b4d912ea32a0b5d9d717"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

temp_user = {
    "admin": {
        "username": "admin",
        "email": "admin@admin.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(temp_user, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(crud.get_current_active_user)):
    return current_user

@app.post("/values/", response_model=schemas.Value)
def create_value(value: schemas.ValueCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        return crud.create_value(db=db, value=value)

@app.get("/values/", response_model=List[schemas.Value])
def read_values(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
            values = crud.get_values(db, skip=skip, limit=limit)
            return values

@app.get("/values/{value_id}", response_model=schemas.Value)
def read_value(value_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        db_value = crud.get_value(db, value_id=value_id)
        if db_value is None:
            raise HTTPException(status_code=404, detail="Value not found")
        return db_value

@app.put("/values/{value_id}", response_model=schemas.Value)
def update_value(value: schemas.ValueCreate, value_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        db_value = crud.update_value(db, value_id=value_id, value=value)
        if db_value is None:
            raise HTTPException(status_code=404, detail="Value not found")
        return db_value

@app.delete("/values/{value_id}", response_model=schemas.Value)
def delete_value(value_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        db_value = crud.delete_value(db, value_id=value_id)
        if db_value is None:
            raise HTTPException(status_code=404, detail="Value not found")
        return db_value

@app.post("/principles/", response_model=schemas.Principle)
def create_principle(principle: schemas.PrincipleCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        return crud.create_principle(db=db, principle=principle)

@app.get("/principles/", response_model=List[schemas.Principle])
def read_principles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        principles = crud.get_principles(db, skip=skip, limit=limit)
        return principles

@app.get("/principles/{principle_id}", response_model=schemas.Principle)
def read_principle(principle_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        db_principle = crud.get_principle(db, principle_id=principle_id)
        if db_principle is None:
            raise HTTPException(status_code=404, detail="Principle not found")
        return db_principle

@app.put("/principles/{principle_id}", response_model=schemas.Principle)
def update_principle(principle: schemas.PrincipleCreate, principle_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        db_principle = crud.update_principle(db, principle_id=principle_id, principle=principle)
        if db_principle is None:
            raise HTTPException(status_code=404, detail="Principle not found")
        return db_principle

@app.delete("/principles/{principle_id}", response_model=schemas.Principle)
def delete_principle(principle_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user), request: Request = Request):
    if current_user and crud.is_permitted(request.method, current_user):
        db_principle = crud.delete_principle(db, principle_id=principle_id)
        if db_principle is None:
            raise HTTPException(status_code=404, detail="Principle not found")
        return db_principle