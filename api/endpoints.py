
from fastapi import APIRouter, UploadFile, File, Response
from analysis.analyzer import Analyzer
from models import Session
from models.Alert import Alert, SessionLocal
from utils.helpers import get_issues_over_time
from visualization.graph_generator import GraphGenerator
from visualization.graph_types import GraphType
from models.Alert import Alert
router = APIRouter()
import os
import io
from fastapi import Form
from fastapi.responses import StreamingResponse
from models.Session import Session as SessionModel
from sqlalchemy.orm import Session
"""@router.post("/analyze", response_class=StreamingResponse)
async def analyze(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    analysis_results = analyzer.analyze_files([await f.read() for f in files], [f.filename for f in files])
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    analysis_results["issues_over_time"] = issues_over_time  # <-- Use DB data here!
    graph_gen = GraphGenerator(analysis_results)
    # Generate and save all graphs
    graph_gen.generate(GraphType.HISTOGRAM)
    graph_gen.generate(GraphType.PIE)
    graph_gen.generate(GraphType.BAR)
    graph_gen.generate(GraphType.LINE)
    img_bytes = graph_gen.generate(GraphType.HISTOGRAM)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")


@router.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    results = analyzer.analyze_files(file_contents, file_names)
    issues = results["issues"]

    db: Session = SessionLocal()
    session = SessionModel()
    db.add(session)
    db.commit()
    db.refresh(session)
    session_id = session.id  # Store the id before closing the session
    for issue in issues:
        alert = Alert(
            description=issue["description"],
            severity=issue["severity"],
            line_number=issue.get("line_number"),
            file_name=issue["file_name"],
            session_id=session_id
        )
        db.add(alert)
    db.commit()
    db.close()
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    alert_lines = [f"{issue['description']} (File: {issue['file_name']})" for issue in issues]
    content = "\n".join(alert_lines)

    os.makedirs("alert", exist_ok=True)
    file_name = f"alerts_{session_id}.txt"
    file_path = os.path.join("alert", file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    file_like = io.BytesIO(content.encode("utf-8"))
    return StreamingResponse(file_like, media_type="text/plain")

from models.Session import Session as SessionModel
from sqlalchemy.orm import joinedload, Session

def get_issues_over_time(db: Session):
    sessions = db.query(SessionModel).options(joinedload(SessionModel.alerts)).order_by(SessionModel.id).all()
    return [len(session.alerts) for session in sessions]"""
# Place these imports at the top if not already present
import os
import io

"""@router.post("/analyze", response_class=StreamingResponse)
async def analyze(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    analysis_results = analyzer.analyze_files(file_contents, file_names)
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    analysis_results["issues_over_time"] = issues_over_time

    # Get upload folder from first file
    upload_folder = os.path.dirname(file_names[0])
    os.makedirs(upload_folder, exist_ok=True)

    # Pass upload_folder to GraphGenerator
    graph_gen = GraphGenerator(analysis_results, output_dir=upload_folder)
    graph_gen.generate(GraphType.HISTOGRAM)
    graph_gen.generate(GraphType.PIE)
    graph_gen.generate(GraphType.BAR)
    graph_gen.generate(GraphType.LINE)
    img_bytes = graph_gen.generate(GraphType.HISTOGRAM)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")
"""
"""@router.post("/analyze", response_class=StreamingResponse)
async def analyze(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    analysis_results = analyzer.analyze_files(file_contents, file_names)
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    analysis_results["issues_over_time"] = issues_over_time

    # Use default 'graphs' folder if no directory in file name
    upload_folder = os.path.dirname(file_names[0]) or "graphs"
    os.makedirs(upload_folder, exist_ok=True)

    graph_gen = GraphGenerator(analysis_results, output_dir=upload_folder)
    graph_gen.generate(GraphType.HISTOGRAM)
    graph_gen.generate(GraphType.PIE)
    graph_gen.generate(GraphType.BAR)
    graph_gen.generate(GraphType.LINE)
    img_bytes = graph_gen.generate(GraphType.HISTOGRAM)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

@router.post("/analyze", response_class=StreamingResponse)
async def analyze(
    files: list[UploadFile] = File(...),
    project_root: str = Form(...)
):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    analysis_results = analyzer.analyze_files(file_contents, file_names)
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    analysis_results["issues_over_time"] = issues_over_time
    graphs_dir = os.path.join(project_root, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    graph_gen = GraphGenerator(analysis_results, output_dir=graphs_dir)
    graph_gen.generate(GraphType.HISTOGRAM)
    graph_gen.generate(GraphType.PIE)
    graph_gen.generate(GraphType.BAR)
    graph_gen.generate(GraphType.LINE)
    img_bytes = graph_gen.generate(GraphType.HISTOGRAM)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")"""
from fastapi.responses import JSONResponse

@router.post("/analyze")
async def analyze(
    files: list[UploadFile] = File(...),
    project_root: str = Form(...)
):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    analysis_results = analyzer.analyze_files(file_contents, file_names)
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    analysis_results["issues_over_time"] = issues_over_time
    graphs_dir = os.path.join(project_root, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    print("%%%% FILE CONTENTS DEBUG %%%%")
    for i, content in enumerate(file_contents):
        print(f"File: {file_names[i]}, Length: {len(content)}, Preview: {content[:100]!r}")
    graph_gen = GraphGenerator(analysis_results, output_dir=graphs_dir)
    graph_gen.generate(GraphType.HISTOGRAM)
    graph_gen.generate(GraphType.PIE)
    graph_gen.generate(GraphType.BAR)
    graph_gen.generate(GraphType.LINE)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("function_lengths:", analysis_results["function_lengths"])
    print("issues_per_type:", analysis_results["issues_per_type"])
    print("issues_per_file:", analysis_results["issues_per_file"])
    return JSONResponse(
        content={"message": f"Graphs saved in {graphs_dir}"}
    )



"""@router.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    results = analyzer.analyze_files(file_contents, file_names)
    issues = results["issues"]

    db: Session = SessionLocal()
    session = SessionModel()
    db.add(session)
    db.commit()
    db.refresh(session)
    session_id = session.id
    for issue in issues:
        alert = Alert(
            description=issue["description"],
            severity=issue["severity"],
            line_number=issue.get("line_number"),
            file_name=issue["file_name"],
            session_id=session_id
        )
        db.add(alert)
    db.commit()
    db.close()
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    alert_lines = [f"{issue['description']} (File: {issue['file_name']})" for issue in issues]
    content = "\n".join(alert_lines)

    # Get upload folder from first file
    upload_folder = os.path.dirname(file_names[0])
    os.makedirs(upload_folder, exist_ok=True)

    # Save alerts file in upload folder
    file_name = f"alerts_{session_id}.txt"
    file_path = os.path.join(upload_folder, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Pass upload_folder to GraphGenerator if you want to generate graphs here too
    # graph_gen = GraphGenerator(results, output_dir=upload_folder)
    # graph_gen.generate(GraphType.LINE)
    # ...

    file_like = io.BytesIO(content.encode("utf-8"))
    return StreamingResponse(file_like, media_type="text/plain")"""

"""@router.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    results = analyzer.analyze_files(file_contents, file_names)
    issues = results["issues"]

    db: Session = SessionLocal()
    session = SessionModel()
    db.add(session)
    db.commit()
    db.refresh(session)
    session_id = session.id
    for issue in issues:
        alert = Alert(
            description=issue["description"],
            severity=issue["severity"],
            line_number=issue.get("line_number"),
            file_name=issue["file_name"],
            session_id=session_id
        )
        db.add(alert)
    db.commit()
    db.close()
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    alert_lines = [f"{issue['description']} (File: {issue['file_name']})" for issue in issues]
    content = "\n".join(alert_lines)

    # Get upload folder from first file, fallback to 'alert' if empty
    upload_folder = os.path.dirname(file_names[0]) or "alert"
    os.makedirs(upload_folder, exist_ok=True)

    # Save alerts file in upload folder
    file_name = f"alerts_{session_id}.txt"
    file_path = os.path.join(upload_folder, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    file_like = io.BytesIO(content.encode("utf-8"))
    return StreamingResponse(file_like, media_type="text/plain")"""
@router.post("/alerts")
async def alerts(
    files: list[UploadFile] = File(...),
    project_root: str = Form(...)
):
    analyzer = Analyzer()
    file_contents = [await f.read() for f in files]
    file_names = [f.filename for f in files]
    results = analyzer.analyze_files(file_contents, file_names)
    issues = results["issues"]

    db: Session = SessionLocal()
    session = SessionModel()
    db.add(session)
    db.commit()
    db.refresh(session)
    session_id = session.id
    for issue in issues:
        alert = Alert(
            description=issue["description"],
            severity=issue["severity"],
            line_number=issue.get("line_number"),
            file_name=issue["file_name"],
            session_id=session_id
        )
        db.add(alert)
    db.commit()
    db.close()
    db: Session = SessionLocal()
    issues_over_time = get_issues_over_time(db)
    db.close()
    alert_lines = [f"{issue['description']} (File: {issue['file_name']})" for issue in issues]
    content = "\n".join(alert_lines)

    # Use project_root/alert as the directory
    alert_dir = os.path.join(project_root, "alert")
    os.makedirs(alert_dir, exist_ok=True)
    file_name = f"alerts_{session_id}.txt"
    file_path = os.path.join(alert_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    file_like = io.BytesIO(content.encode("utf-8"))
    return StreamingResponse(file_like, media_type="text/plain")