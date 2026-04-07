from database.db import db
from datetime import datetime

class NewReferral(db.Model):
    __tablename__ = 'new_referrals'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    student_class = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    behavior = db.Column(db.String(255), nullable=True)
    academic = db.Column(db.String(255), nullable=True)

    # ✅ New fields
    counselor_email = db.Column(db.String(120), nullable=True)
    doctor_email = db.Column(db.String(120), nullable=True)
    suggestion = db.Column(db.Text, nullable=True)
    precautions = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'unique_id': self.unique_id,
            'name': self.name,
            'age': self.age,
            'student_class': self.student_class,
            'address': self.address,
            'reason': self.reason,
            'behavior': self.behavior,
            'academic': self.academic,
            'counselor_email': self.counselor_email,
            'doctor_email': self.doctor_email,
            'suggestion': self.suggestion,
            'precautions': self.precautions,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
        }