from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = "9d86100bb6719b26e286af2eaa35a11f68878cb85f88b4d912ea32a0b5d9d717"
ALGORITHM = "HS256"

temp_user = {
    "admin": {
        "username": "admin",
        "email": "admin@admin.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "permissions": ["GET", "POST", "PUT", "DELETE"]
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

try:
    from . import models, schemas
except ImportError:
    import models, schemas

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)

def authenticate_user(temp_user, username: str, password: str):
    user = get_user(temp_user, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(temp_user, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def is_permitted(request: str, current_user: schemas.User = Depends(get_current_user)):
    if request in current_user.permissions:
        return True
    else:
        raise HTTPException(status_code=401, detail="You have are not permitted to do this action.")

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
    return (
        db.query(models.Principle).filter(models.Principle.id == principle_id).first()
    )


def get_principles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Principle).offset(skip).limit(limit).all()


def create_principle(db: Session, principle: schemas.PrincipleCreate):
    db_principle = models.Principle(
        title=principle.title, description=principle.description
    )
    db.add(db_principle)
    db.commit()
    db.refresh(db_principle)
    return db_principle


def update_principle(
    db: Session, principle_id: int, principle: schemas.PrincipleCreate
):
    db_principle = (
        db.query(models.Principle).filter(models.Principle.id == principle_id).first()
    )
    if db_principle is not None:
        db_principle.title = principle.title
        db_principle.description = principle.description
        db.commit()
        db.refresh(db_principle)
        return db_principle


def delete_principle(db: Session, principle_id: int):
    db_principle = (
        db.query(models.Principle).filter(models.Principle.id == principle_id).first()
    )
    if db_principle is not None:
        db.delete(db_principle)
        db.commit()
        return db_principle
