from flask import Flask
from config import Config
from weather.views import main_blueprint
import logging
import os
import glob
from datetime import datetime

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    app.register_blueprint(main_blueprint)

    # Set up a dedicated logs directory
    LOG_DIR = 'logs'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Create a unique log filename for the current session using a timestamp
    session_log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    # Configure logging to output to the session log file
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=session_log_file
    )

    # Function to clean up old log files, keeping only the latest 30 sessions
    def cleanup_old_logs(max_logs=30):
        log_files = sorted(glob.glob(os.path.join(LOG_DIR, "app_*.log")))
        while len(log_files) > max_logs:
            os.remove(log_files[0])
            log_files.pop(0)

    cleanup_old_logs()

    return app

