#detectors.py
import ast
import re

MAX_FUNCTION_LENGTH = 20
MAX_FILE_LENGTH = 400

def function_length_detector(file_path):
    """
    Detects functions in the file that are longer than MAX_FUNCTION_LENGTH lines.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: List of issues found, each as a dict.
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
                issues.append({
                    "issue_type": "FunctionTooLong",
                    "description": f"Function '{node.name}' is too long ({length} lines)",
                    "severity": "warning",
                    "line_number": start_line,
                    "function_length": length
                })
    return issues

def file_length_detector(file_path):
    """
    Detects if the file exceeds MAX_FILE_LENGTH lines.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: List with a single issue dict if file is too long, else empty list.
    """
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > MAX_FILE_LENGTH:
        return [{
            "issue_type": "FileTooLong",
            "description": f"File is too long ({len(lines)} lines)",
            "severity": "info",
            "line_number": None
        }]
    return []

def unused_variable_detector(file_path):
    """
    Detects variables that are assigned but never used in the file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: List of issues found, each as a dict.
    """
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    assigned = set()
    used = set()
    class VarVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                assigned.add((node.id, node.lineno))
            elif isinstance(node.ctx, ast.Load):
                used.add(node.id)
    VarVisitor().visit(tree)
    unused = [(name, lineno) for name, lineno in assigned if name not in used and not name.startswith('_')]
    issues = []
    for name, lineno in unused:
        issues.append({
            "issue_type": "UnusedVariable",
            "description": f"Variable '{name}' is assigned but never used",
            "severity": "warning",
            "line_number": lineno
        })
    return issues

def docstring_detector(file_path):
    """
    Detects functions that are missing a docstring.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: List of issues found, each as a dict.
    """
    issues = []
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                issues.append({
                    "issue_type": "MissingDocstring",
                    "description": f"Function '{node.name}' is missing a docstring",
                    "severity": "info",
                    "line_number": node.lineno
                })
    return issues

def non_english_var_detector(file_path):
    """
    Detects variable names that contain non-English (non-ASCII) characters.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: List of issues found, each as a dict.
    """
    issues = []
    non_english_pattern = re.compile(r'[^\x00-\x7F]')
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if non_english_pattern.search(node.id):
                issues.append({
                    "issue_type": "NonEnglishVariable",
                    "description": f"Variable '{node.id}' is not in English",
                    "severity": "warning",
                    "line_number": node.lineno
                })
    return issues