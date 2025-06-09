from .detectors import function_length_detector, file_length_detector, unused_variable_detector, non_english_var_detector, docstring_detector
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

