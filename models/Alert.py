from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey,create_engine
from sqlalchemy.orm import relationship
from .Session import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    line_number = Column(Integer, nullable=True)
    file_name = Column(String, nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="alerts")

# Database setup
DATABASE_URL = "mssql+pyodbc://localhost/IssusesInPython2?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)