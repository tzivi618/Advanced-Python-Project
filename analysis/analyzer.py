"""from .detectors import function_length_detector, file_length_detector, unused_variable_detector, non_english_var_detector, docstring_detector
class Analyzer:
    def __init__(self):
        self.detectors = [
            function_length_detector(),
            file_length_detector(),
            unused_variable_detector(),
            non_english_var_detector(),
            docstring_detector()
        ]

    def analyze(self, file_path):
        issues = []
        for detector in self.detectors:
            issues.extend(detector.detect(file_path))
        return issues

from .detectors import function_length_detector, file_length_detector, unused_variable_detector, non_english_var_detector, docstring_detector

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


# analysis/analyzer.py

from .detectors import function_length_detector, file_length_detector, unused_variable_detector, non_english_var_detector, docstring_detector

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

    def analyze_files(self, file_contents, file_names):
        # file_contents: list of bytes, file_names: list of str
        import tempfile, os
        all_issues = []
        function_lengths = []
        issues_per_type = {}
        issues_per_file = {}
        for content, name in zip(file_contents, file_names):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
                tmp.write(content.decode("utf-8"))
                tmp_path = tmp.name
            issues = self.analyze(tmp_path)
            all_issues.extend(issues)
            issues_per_file[name] = len(issues)
            for issue in issues:
                issues_per_type[issue["issue_type"]] = issues_per_type.get(issue["issue_type"], 0) + 1
            # For histogram
            for detector in self.detectors:
                if detector.__name__ == "function_length_detector":
                    for node_issue in detector(tmp_path):
                        desc = node_issue.get("description", "")
                        import re
                        match = re.search(r"\((\d+) lines\)", desc)
                        if match:
                            function_lengths.append(int(match.group(1)))
            os.unlink(tmp_path)
        return {
            "issues": all_issues,
            "function_lengths": function_lengths,
            "issues_per_type": issues_per_type,
            "issues_per_file": issues_per_file
        }
"""

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

    def analyze_files(self, file_contents, file_names):
        all_issues = []
        function_lengths = []
        issues_per_type = {}
        issues_per_file = {}

        for content, name in zip(file_contents, file_names):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
                tmp.write(content.decode("utf-8"))
                tmp_path = tmp.name

            issues = self.analyze(tmp_path)
            all_issues.extend(issues)
            issues_per_file[name] = len(issues)
            for issue in issues:
                issues_per_type[issue["issue_type"]] = issues_per_type.get(issue["issue_type"], 0) + 1
                # לאסוף אורכי פונקציות לגרף
                if issue["issue_type"] == "FunctionTooLong" and "function_length" in issue:
                    function_lengths.append(issue["function_length"])
            # אפשר גם לאסוף אורכי כל הפונקציות (לא רק החריגות) אם רוצים
            # כאן נאספים רק אלו שעברו את הסף
            os.unlink(tmp_path)

        return {
            "issues": all_issues,
            "function_lengths": function_lengths,
            "issues_per_type": issues_per_type,
            "issues_per_file": issues_per_file
        }