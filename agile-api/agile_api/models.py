from sqlalchemy import Column, Integer, String, Text
from database import Base

class Value(Base):
    __tablename__ = "values"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, index=True)

class Principle(Base):
    __tablename__ = "principles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, index=True)

