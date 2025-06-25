# models/Session.py
"""from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .Alert import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path_id = Column(Integer, ForeignKey("paths.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    alerts = relationship("Alert", back_populates="session")
    path = relationship("Path")"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .Base import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path_id = Column(Integer, ForeignKey("paths.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    alerts = relationship("Alert", back_populates="session")
    path = relationship("Path")