import io
import os
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, File, Response
from fastapi.responses import StreamingResponse, JSONResponse
from analysis.analyzer import Analyzer
from models.Alert import Alert, SessionLocal
from visualization.graph_generator import GraphGenerator
from visualization.graph_types import GraphType
from .schemas import AnalyzeResponse, AlertResponse

router = APIRouter()

@router.post("/analyze", response_class=StreamingResponse)
async def analyze(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    analysis_results = analyzer.analyze_files([await f.read() for f in files], [f.filename for f in files])
    graph_gen = GraphGenerator(analysis_results)
    # Generate and save all graphs
    graph_gen.generate(GraphType.HISTOGRAM)
    graph_gen.generate(GraphType.PIE)
    graph_gen.generate(GraphType.BAR)
    graph_gen.generate(GraphType.LINE)
    # Return one of them (e.g., histogram) as response
    img_bytes = graph_gen.generate(GraphType.HISTOGRAM)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

from fastapi.responses import StreamingResponse

"""@router.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    results = analyzer.analyze_files([await f.read() for f in files], [f.filename for f in files])
    issues = results["issues"]
    alert_lines = [issue["description"] for issue in issues]
    content = "\n".join(alert_lines)

    # Ensure the alerts directory exists
    os.makedirs("alerts", exist_ok=True)
    # Save alerts to file
    with open("alerts/alerts.txt", "w", encoding="utf-8") as f:
        f.write(content)

    file_like = io.BytesIO(content.encode("utf-8"))
    headers = {
        "Content-Disposition": "attachment; filename=alerts.txt"
    }
    return Response(content, media_type="text/plain")"""
from sqlalchemy.orm import Session
from models.Alert import Alert

@router.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    results = analyzer.analyze_files([await f.read() for f in files], [f.filename for f in files])
    issues = results["issues"]

    # Save alerts to the database
    db: Session = SessionLocal()
    for issue in issues:
        alert = Alert(
            description=issue["description"],
            severity=issue["severity"],
            line_number=issue.get("line_number")
        )
        db.add(alert)
    db.commit()
    db.close()

    # Return alerts as a downloadable file
    alert_lines = [issue["description"] for issue in issues]
    content = "\n".join(alert_lines)
    file_like = io.BytesIO(content.encode("utf-8"))
    headers = {
        "Content-Disposition": "attachment; filename=alerts.txt"
    }
    return StreamingResponse(file_like, media_type="text/plain", headers=headers)