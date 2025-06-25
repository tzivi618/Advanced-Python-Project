#issue.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Issue:
    issue_type: str
    description: str
    severity: str = "warning"
    line_number: Optional[int] = None
    timestamp: Optional[str] = None

    def __str__(self):
        return f"[{self.severity}] {self.issue_type} (line {self.line_number}): {self.description}"