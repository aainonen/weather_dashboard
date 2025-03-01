from flask import Flask
from config import Config
from weather.views import main_blueprint

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    app.register_blueprint(main_blueprint)
    return app
