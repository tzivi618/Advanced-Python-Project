from detectors import function_length_detector, file_length_detector,unused_variable_detector,DocstringDetector,NonEnglishVarDetector

class Analyzer:
    def __init__(self):
        self.detectors = [
            function_length_detector(),
            file_length_detector(),
            unused_variable_detector(),
            DocstringDetector(),
            NonEnglishVarDetector()
        ]

    def analyze(self, file_path):
        issues = []
        for detector in self.detectors:
            issues.extend(detector.detect(file_path))
        return issues