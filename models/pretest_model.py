from database.db import db
from datetime import datetime

class PretestResult(db.Model):
    __tablename__ = 'pretest_results'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)

    # Now stores full structured answers JSON
    answers = db.Column(db.Text, nullable=False)

    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)