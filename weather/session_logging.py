# weather/session_logging.py
from flask import request, current_app, g
from datetime import datetime
import time

from .models import SessionMetric
from . import db

def register_session_logging(app):
    @app.before_request
    def start_timer():
        g.session_start_time = time.time()

    @app.after_request
    def log_session(response):
        session_end_time = time.time()
        duration = session_end_time - g.session_start_time

        ip = request.remote_addr or 'unknown'
        user_agent = request.headers.get('User-Agent', 'unknown')
        is_bot = 'bot' in user_agent.lower()

        session_metric = SessionMetric(
            ip_address=ip,
            user_agent=user_agent,
            is_bot=is_bot,
            session_start=datetime.utcfromtimestamp(g.session_start_time),
            session_end=datetime.utcnow(),
            session_duration=duration
        )

        try:
            db.session.add(session_metric)
            db.session.commit()
            current_app.logger.info("Logged session: IP=%s, Duration=%.2fs", ip, duration)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Failed to log session: %s", e)

        return response
