import ast
from models.issue import Issue

def docstring_detector(file_path):
    """
    Detects functions that do not have a docstring.
    """
    issues = []
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and ast.get_docstring(node) is None:
            issues.append(Issue(
                issue_type="MissingDocstring",
                description=f"Function '{node.name}' is missing a docstring",
                severity="info",
                line_number=node.lineno
            ))
    return issues
