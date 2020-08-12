from typing import Optional
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
