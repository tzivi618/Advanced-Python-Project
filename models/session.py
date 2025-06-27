from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Session(Base):
    """
    Represents a single analysis session for a given path.
    """
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path_id = Column(Integer, ForeignKey("paths.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    path = relationship("Path", back_populates="sessions")
    alerts = relationship("Alert", back_populates="session", cascade="all, delete-orphan")
