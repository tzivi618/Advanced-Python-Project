from dataclasses import dataclass
from typing import Optional
from models.Issue import Issue

@dataclass
class FileIssues(Issue):
    file_name: str=""

    def __str__(self):
        base = super().__str__()
        return f"{base} | file: {self.file_name}"