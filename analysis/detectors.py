import ast
import re

def function_length_detector(file_path):
    issues = []
    with open(file_path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start_line)
            length = end_line - start_line + 1
            if length > 20:
                issues.append({
                    "issue_type": "FunctionTooLong",
                    "description": f"Function '{node.name}' is too long ({length} lines)",
                    "severity": "warning",
                    "line_number": start_line
                })
    return issues

def file_length_detector(file_path):
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > 200:
        return [{
            "issue_type": "FileTooLong",
            "description": f"File is too long ({len(lines)} lines)",
            "severity": "info",
            "line_number": None
        }]
    return []

def unused_variable_detector(file_path):
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

