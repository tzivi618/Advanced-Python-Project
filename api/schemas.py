from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    """
    Input schema for analyze endpoint.
    """
    file_path: str

class IssueSchema(BaseModel):
    """
    Schema for a single issue reported by the analyzer.
    """
    issue_type: str
    description: str
    severity: str
    line_number: Optional[int] = None
    timestamp: Optional[str] = None

class AnalyzeResponse(BaseModel):
    """
    Output schema for analyze response.
    """
    issues: List[IssueSchema]

class AlertResponse(BaseModel):
    """
    Output schema for alert response.
    """
    alerts: List[str]
