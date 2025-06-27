import ast
from models.issue import Issue

def unused_variable_detector(file_path):
    """
    Detects variables that are assigned but never used.
    """
    issues = []
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
    for name, lineno in unused:
        issues.append(Issue(
            issue_type="UnusedVariable",
            description=f"Variable '{name}' is assigned but never used",
            severity="warning",
            line_number=lineno
        ))
    return issues
