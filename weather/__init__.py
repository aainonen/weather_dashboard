from flask import Flask
from config import Config
from weather.views import main_blueprint
import logging

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    app.register_blueprint(main_blueprint)

    # Configure basic logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    return app

