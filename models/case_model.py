from database.db import db
from datetime import datetime

class CaseScenarioResult(db.Model):
    __tablename__ = 'case_results'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    answers = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)