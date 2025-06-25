#graph_types.py
from enum import Enum

class GraphType(Enum):
    HISTOGRAM = "histogram"
    PIE = "pie"
    BAR = "bar"
    LINE = "line"