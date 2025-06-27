from pydantic import BaseModel
from typing import Optional

class Issue(BaseModel):
    """
    Represents an issue found during static code analysis.
    """
    issue_type: str
    description: str
    severity: str
    line_number: Optional[int] = None
    file_name: Optional[str] = None
    extra: dict = {}

    def to_dict(self):
        """
        Converts the Issue instance to a dictionary.
        """
        return self.dict()
