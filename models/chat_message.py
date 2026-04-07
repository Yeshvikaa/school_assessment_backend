from database.db import db
from datetime import datetime

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)

    # link to referral
    referral_unique_id = db.Column(db.Integer, nullable=False)

    sender_email = db.Column(db.String(120), nullable=False)
    receiver_email = db.Column(db.String(120), nullable=False)

    message = db.Column(db.Text, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "referral_unique_id": self.referral_unique_id,
            "sender_email": self.sender_email,
            "receiver_email": self.receiver_email,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }