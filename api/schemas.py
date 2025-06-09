from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    file_path: str

class IssueSchema(BaseModel):
    issue_type: str
    description: str
    severity: str
    line_number: Optional[int] = None
    timestamp: Optional[str] = None

class AnalyzeResponse(BaseModel):
    issues: List[IssueSchema]

class AlertResponse(BaseModel):
    alerts: List[str]