# analysis/results.py
class AnalysisResult:
    def __init__(self, issues):
        self.issues = issues

    def to_dict(self):
        return {"issues": self.issues}