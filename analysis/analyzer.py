from .detectors import (
    function_length_detector,
    file_length_detector,
    unused_variable_detector,
    non_english_var_detector,
    docstring_detector
)

import tempfile
import os
import re
import ast
class Analyzer:
    def __init__(self):
        self.detectors = [
            function_length_detector,
            file_length_detector,
            unused_variable_detector,
            non_english_var_detector,
            docstring_detector
        ]

    def analyze(self, file_path):
        issues = []
        for detector in self.detectors:
            issues.extend(detector(file_path))
        return issues

    """def analyze_files(self, file_contents, file_names):
        all_issues = []
        function_lengths = []
        issues_per_type = {}
        issues_per_file = {}
        issues_over_time = []
        for content, name in zip(file_contents, file_names):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
                tmp.write(content.decode("utf-8"))
                tmp_path = tmp.name
            issues = self.analyze(tmp_path)
            all_issues.extend(issues)
            issues_per_file[name] = len(issues)
            for issue in issues:
                issues_per_type[issue["issue_type"]] = issues_per_type.get(issue["issue_type"], 0) + 1
                if issue["issue_type"] == "FunctionTooLong" and "function_length" in issue:
                    function_lengths.append(issue["function_length"])
            os.unlink(tmp_path)

        return {
            "issues": all_issues,
            "function_lengths": function_lengths,
            "issues_per_type": issues_per_type,
            "issues_per_file": issues_per_file
        }"""

    def analyze_files(self, file_contents, file_names):
        all_issues = []
        function_lengths = []
        issues_per_type = {}
        issues_per_file = {}
        issues_over_time = []

        for content, name in zip(file_contents, file_names):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
                tmp.write(content.decode("utf-8"))
                tmp_path = tmp.name

            # Collect all function lengths
            with open(tmp_path, encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    start_line = node.lineno
                    end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start_line)
                    length = end_line - start_line + 1
                    function_lengths.append(length)

            issues = self.analyze(tmp_path)
            all_issues.extend(issues)
            issues_per_file[name] = len(issues)
            issues_over_time.append(len(issues))  # Add this line
            for issue in issues:
                issues_per_type[issue["issue_type"]] = issues_per_type.get(issue["issue_type"], 0) + 1

            os.unlink(tmp_path)

        return {
            "issues": all_issues,
            "function_lengths": function_lengths,
            "issues_per_type": issues_per_type,
            "issues_per_file": issues_per_file,
            "issues_over_time": issues_over_time  # Add this line
        }
"""
import ast

def analyze_files(self, file_contents, file_names):
    all_issues = []
    function_lengths = []
    issues_per_type = {}
    issues_per_file = {}

    for content, name in zip(file_contents, file_names):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
            tmp.write(content.decode("utf-8"))
            tmp_path = tmp.name

        # Collect all function lengths for the histogram
        with open(tmp_path, encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno
                end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start_line)
                length = end_line - start_line + 1
                function_lengths.append(length)

        issues = self.analyze(tmp_path)
        all_issues.extend(issues)
        issues_per_file[name] = len(issues)
        for issue in issues:
            issues_per_type[issue["issue_type"]] = issues_per_type.get(issue["issue_type"], 0) + 1

        os.unlink(tmp_path)

    return {
        "issues": all_issues,
        "function_lengths": function_lengths,
        "issues_per_type": issues_per_type,
        "issues_per_file": issues_per_file
    }


def analyze_files(self, file_contents, file_names):
    all_issues = []
    function_lengths = []
    issues_per_type = {}
    issues_per_file = {}

    for content, name in zip(file_contents, file_names):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
            tmp.write(content.decode("utf-8"))
            tmp_path = tmp.name

        # Collect all function lengths for the histogram
        with open(tmp_path, encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno
                end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start_line)
                length = end_line - start_line + 1
                function_lengths.append(length)

        issues = self.analyze(tmp_path)
        all_issues.extend(issues)
        issues_per_file[name] = len(issues)
        for issue in issues:
            issues_per_type[issue["issue_type"]] = issues_per_type.get(issue["issue_type"], 0) + 1

        os.unlink(tmp_path)

    return {
        "issues": all_issues,
        "function_lengths": function_lengths,
        "issues_per_type": issues_per_type,
        "issues_per_file": issues_per_file
    }"""