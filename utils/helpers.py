# utils/helpers.py
from models.Path import Path
from models.Session import Session as SessionModel

def get_or_create_path(db, project_root):
    path = db.query(Path).filter_by(path=project_root).first()
    if not path:
        path = Path(path=project_root)
        db.add(path)
        db.commit()
        db.refresh(path)
    return path

def get_issues_over_time(db, project_root):
    path = db.query(Path).filter_by(path=project_root).first()
    if not path:
        return []
    sessions = db.query(SessionModel).filter_by(path_id=path.id).order_by(SessionModel.id).all()
    return [len(session.alerts) for session in sessions]