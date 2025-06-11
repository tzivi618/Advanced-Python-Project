"""from .Issue import Issue
from .FunctionIssues import FunctionIssues
from .FileIssues import FileIssues"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .Base import Base
from .Alert import Alert
from .Session import Session
from .Path import Path

DATABASE_URL = "mssql+pyodbc://localhost/IssuesInPython3?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)