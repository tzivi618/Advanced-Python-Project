from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Path(Base):
    """
    Represents a root path (project folder) being analyzed.
    """
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255), unique=True, nullable=False)
    sessions = relationship("Session", back_populates="path", cascade="all, delete-orphan")
