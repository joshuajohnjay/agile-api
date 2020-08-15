from typing import Optional, List
from pydantic import BaseModel


class ValueBase(BaseModel):
    title: str
    description: Optional[str] = None


class ValueCreate(ValueBase):
    pass


class Value(ValueBase):
    id: int

    class Config:
        orm_mode = True


class PrincipleBase(BaseModel):
    title: str
    description: Optional[str] = None


class PrincipleCreate(PrincipleBase):
    pass


class Principle(PrincipleBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None
    permissions: List[str] = None

class UserInDB(User):
    hashed_password: str