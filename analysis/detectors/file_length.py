from models.issue import Issue

MAX_FILE_LENGTH = 400

def file_length_detector(file_path):
    """
    Detects if the file exceeds the maximum allowed number of lines.
    """
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > MAX_FILE_LENGTH:
        return [Issue(
            issue_type="FileTooLong",
            description=f"File is too long ({len(lines)} lines)",
            severity="info",
            line_number=None
        )]
    return []
