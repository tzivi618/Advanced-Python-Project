import os
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from analysis.analyzer import Analyzer
from models import SessionLocal
from models.session import Session as SessionModel
from models.alert import Alert
from utils.helpers import get_or_create_path, get_issues_over_time
from visualization.graph_generator import GraphGenerator
from visualization.graph_types import GraphType
from datetime import datetime


def get_output_dir(project_root: str, session_id: int = None, is_preview=False) -> str:
    """
    Creates and returns an output directory path for storing results.
    """
    if is_preview:
        output_dir = os.path.join(project_root, "results", "preview")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(project_root, "results", timestamp)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


async def read_uploaded_files(files):
    """
    Reads uploaded files and returns their contents and filenames.
    """
    contents = [await f.read() for f in files]
    filenames = [f.filename for f in files]
    return contents, filenames


def save_alerts_to_db(db: Session, issues, session_id: int):
    """
    Saves a list of issues into the database as alerts.
    """
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


def save_alerts_txt(issues, output_dir, filename):
    """
    Saves alerts to a text file in the specified output directory.
    """
    lines = [f"{issue['description']} (File: {issue['file_name']})" for issue in issues]
    content = "\n".join(lines)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return content


def generate_graphs(results, output_dir, types):
    """
    Generates graphs based on the analysis results.
    """
    graph_gen = GraphGenerator(results, output_dir=output_dir)
    for graph_type in types:
        graph_gen.generate(graph_type)


async def process_analysis(files, project_root, is_preview=False, save_to_db=True):
    """
    Processes the analysis workflow and returns a JSON response.
    """
    analyzer = Analyzer()
    contents, filenames = await read_uploaded_files(files)
    results = analyzer.analyze_files(contents, filenames)

    issues = results.get("issues", [])
    errors = results.get("errors", [])

    if not issues:
        return JSONResponse(status_code=400, content={
            "message": "No valid Python files were found or all files failed to analyze.",
            "status": "failed",
            "errors": errors
        })

    output_dir = get_output_dir(project_root, is_preview=is_preview)

    if save_to_db:
        db: Session = SessionLocal()
        path = get_or_create_path(db, project_root)
        session = SessionModel(path_id=path.id)
        db.add(session)
        db.commit()
        db.refresh(session)
        save_alerts_to_db(db, issues, session.id)
        issues_over_time = get_issues_over_time(db, project_root)
        db.close()
        results["issues_over_time"] = issues_over_time
        graph_types = [GraphType.HISTOGRAM, GraphType.PIE, GraphType.BAR]
        if len(issues_over_time) >= 2:
            graph_types.append(GraphType.LINE)
        filename = f"alerts_{session.id}.txt"
    else:
        db: Session = SessionLocal()
        results["issues_over_time"] = get_issues_over_time(db, project_root)
        db.close()
        graph_types = [GraphType.HISTOGRAM, GraphType.PIE, GraphType.BAR]
        filename = "alerts_preview.txt"

    generate_graphs(results, output_dir, graph_types)
    save_alerts_txt(issues, output_dir, filename)

    return JSONResponse(content={
        "message": f"Graphs saved in {output_dir}",
        "status": "success" if not errors else "partial",
        "output_dir": output_dir,
        "errors": errors,
        "issues_summary": {
            "function_lengths": results["function_lengths"],
            "issues_per_type": results["issues_per_type"],
            "issues_per_file": results["issues_per_file"]
        },
        **({"session_id": session.id} if save_to_db else {})
    })


async def handle_alerts(files, project_root):
    """
    Handles analysis request and persists alerts into the database.
    """
    return await process_analysis(files, project_root, is_preview=False, save_to_db=True)


async def handle_analyze(files, project_root):
    """
    Handles a preview analysis request without saving to database.
    """
    return await process_analysis(files, project_root, is_preview=True, save_to_db=False)
