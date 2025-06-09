import io

from fastapi import APIRouter, UploadFile, File, Response
from fastapi.responses import StreamingResponse, JSONResponse
from analysis.analyzer import Analyzer
from visualization.graph_generator import GraphGenerator
from visualization.graph_types import GraphType
from .schemas import AnalyzeResponse, AlertResponse

router = APIRouter()

@router.post("/analyze", response_class=StreamingResponse)
async def analyze(files: list[UploadFile] = File(...)):
    # ניתוח קבצים
    analyzer = Analyzer()
    analysis_results = analyzer.analyze_files([await f.read() for f in files], [f.filename for f in files])
    # יצירת גרפים
    graph_gen = GraphGenerator(analysis_results)
    # דוגמה: מחזירים היסטוגרמה (אפשר להרחיב להחזיר כמה גרפים)
    img_bytes = graph_gen.generate(GraphType.HISTOGRAM)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

@router.post("/alerts", response_model=AlertResponse)
async def alerts(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    issues = analyzer.detect_issues([await f.read() for f in files], [f.filename for f in files])
    return AlertResponse(issues=issues)