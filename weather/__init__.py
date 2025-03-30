# weather/__init__.py

import logging
import os
import glob
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .extensions import limiter  # Import limiter from extensions.py
from .views import main_blueprint

db = SQLAlchemy()

def configure_logging():
    LOG_DIR = 'logs'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    session_log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    # Create a file handler
    file_handler = logging.FileHandler(session_log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # Get the root logger and add the file handler if not already added
    root_logger = logging.getLogger()

    # Remove existing handlers to avoid duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)

    # Optional: Also log to console for debugging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Cleanup old logs
    def cleanup_old_logs(max_logs=30):
        log_files = sorted(glob.glob(os.path.join(LOG_DIR, "app_*.log")))
        while len(log_files) > max_logs:
            os.remove(log_files[0])
            log_files.pop(0)

    cleanup_old_logs()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Limiter
    limiter.init_app(app)

    # Register the main blueprint
    app.register_blueprint(main_blueprint)

    # Register session logging hooks
    from . import session_logging
    session_logging.register_session_logging(app)

    # Configure logging explicitly
    configure_logging()

    @app.after_request
    def add_security_headers(response):
        # Add a Content Security Policy (CSP) header
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "  # Allow content only from the same origin
            "img-src 'self' https://openweathermap.org; "  # Allow images from OpenWeatherMap
            "script-src 'self'; "  # Allow scripts only from the same origin
            "style-src 'self'; "  # Allow styles only from the same origin
        )
        return response

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template('error.html', message="The request is too large. Please try again with a smaller payload."), 413

    return app

