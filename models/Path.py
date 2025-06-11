"""# models/Path.py
from sqlalchemy import Column, Integer, String
from .Alert import Base

class Path(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, unique=True, nullable=False)"""
from sqlalchemy import Column, Integer, String
from .Base import Base

class Path(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255), unique=True, nullable=False)  # Set max length!