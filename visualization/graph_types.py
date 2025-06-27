from enum import Enum

class GraphType(Enum):
    """
    Enumeration of supported graph types for visualization.
    """
    HISTOGRAM = "histogram"
    PIE = "pie"
    BAR = "bar"
    LINE = "line"
