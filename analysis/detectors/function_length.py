import ast
from models.issue import Issue

MAX_FUNCTION_LENGTH = 20

def function_length_detector(file_path):
    """
    Detects functions that are longer than the allowed maximum length.
    """
    issues = []
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start_line)
            length = end_line - start_line + 1
            if length > MAX_FUNCTION_LENGTH:
                issues.append(Issue(
                    issue_type="FunctionTooLong",
                    description=f"Function '{node.name}' is too long ({length} lines)",
                    severity="warning",
                    line_number=start_line,
                    extra={"function_length": length}
                ))
    return issues
