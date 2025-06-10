# In your endpoints or a utils file
from sqlalchemy.orm import Session, joinedload
from models.Session import Session as SessionModel

def get_issues_over_time(db: Session):
    sessions = db.query(SessionModel).options(joinedload(SessionModel.alerts)).order_by(SessionModel.id).all()
    return [len(session.alerts) for session in sessions]