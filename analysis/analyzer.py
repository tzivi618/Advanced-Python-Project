import tempfile, os, ast

class Analyzer:
    """
    Analyzes Python files using a collection of detectors to identify issues such as function length,
    file length, unused variables, and more.
    """
    def __init__(self):
        from .detectors import (
            function_length_detector,
            file_length_detector,
            unused_variable_detector,
            non_english_var_detector,
            docstring_detector,
        )
        self.detectors = [
            function_length_detector,
            file_length_detector,
            unused_variable_detector,
            non_english_var_detector,
            docstring_detector
        ]

    def analyze(self, file_path):
        """
        Applies all detectors to a given file path and returns the list of issues.
        """
        issues = []
        for detector in self.detectors:
            issues.extend(detector(file_path))
        return issues

    def analyze_files(self, file_contents, file_names):
        """
        Analyzes multiple files by writing them to temporary files and collecting issues and metadata.
        """
        all_issues = []
        function_lengths = []
        issues_per_type = {}
        issues_per_file = {}
        issues_over_time = []
        errors = []

        for content, name in zip(file_contents, file_names):
            if not name.endswith(".py"):
                errors.append({
                    "file": name,
                    "error": "Unsupported file type – only .py files are allowed"
                })
                continue

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
                    tmp.write(content.decode("utf-8"))
                    tmp_path = tmp.name

                try:
                    with open(tmp_path, encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            start = node.lineno
                            end = max((n.lineno for n in ast.walk(node) if hasattr(n, "lineno")), default=start)
                            function_lengths.append(end - start + 1)
                except SyntaxError as e:
                    errors.append({
                        "file": name,
                        "error": f"Syntax error: {str(e)}"
                    })
                    os.unlink(tmp_path)
                    continue

                issues = self.analyze(tmp_path)
                for issue in issues:
                    issue.file_name = name

                all_issues.extend(issues)
                issues_per_file[name] = len(issues)
                issues_over_time.append(len(issues))
                for issue in issues:
                    issues_per_type[issue.issue_type] = issues_per_type.get(issue.issue_type, 0) + 1

                os.unlink(tmp_path)

            except Exception as e:
                errors.append({
                    "file": name,
                    "error": f"Unexpected error: {str(e)}"
                })

        return {
            "issues": [i.to_dict() for i in all_issues],
            "function_lengths": function_lengths,
            "issues_per_type": issues_per_type,
            "issues_per_file": issues_per_file,
            "issues_over_time": issues_over_time,
            "errors": errors
        }
