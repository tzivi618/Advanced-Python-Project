#functionIssues.py
from dataclasses import dataclass
from typing import Optional
from models.Issue import Issue

@dataclass
class FunctionIssues(Issue):
    function_name: str = ""
    length: int = 0

    def __str__(self):
        base = super().__str__()
        return f"{base} | function: {self.function_name} (length: {self.length})"