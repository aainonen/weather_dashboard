import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Config:
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your_dummy_api_key')
    DEBUG = os.environ.get('DEBUG', True)
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
        f"@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

