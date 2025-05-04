# weather/models.py
from datetime import datetime
from . import db  # This assumes your __init__.py defines and exposes `db`

class SessionMetric(db.Model):
    __tablename__ = 'session_metric'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv4 and IPv6 support
    user_agent = db.Column(db.String(255))
    is_bot = db.Column(db.Boolean, default=False)
    session_start = db.Column(db.DateTime, default=datetime.utcnow)
    session_end = db.Column(db.DateTime)
    session_duration = db.Column(db.Float)  # In seconds
    search_location = db.Column(db.Text)  # In seconds

    def __repr__(self):
        return f"<SessionMetric {self.id} {self.ip_address}>"

