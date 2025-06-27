from fastapi import APIRouter, UploadFile, File, Form
from api.handlers import handle_analyze, handle_alerts

router = APIRouter()

@router.post("/alerts")
async def alerts(files: list[UploadFile] = File(...), project_root: str = Form(...)):
    """
    API endpoint for saving alerts to the database.
    """
    return await handle_alerts(files, project_root)


@router.post("/analyze")
async def analyze(files: list[UploadFile] = File(...), project_root: str = Form(...)):
    """
    API endpoint for running analysis preview without saving alerts.
    """
    return await handle_analyze(files, project_root)
