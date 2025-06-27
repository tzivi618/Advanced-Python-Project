import ast
import re
from models.issue import Issue

non_english_pattern = re.compile(r'[^\x00-\x7F]')

def non_english_var_detector(file_path):
    """
    Detects variables with non-English names.
    """
    issues = []
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and non_english_pattern.search(node.id):
            issues.append(Issue(
                issue_type="NonEnglishVariable",
                description=f"Variable '{node.id}' is not in English",
                severity="warning",
                line_number=node.lineno
            ))
    return issues
