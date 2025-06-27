from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Alert(Base):
    """
    Represents a detected issue (alert) in a specific file during analysis.
    """
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    line_number = Column(Integer, nullable=True)
    file_name = Column(String, nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="alerts")
