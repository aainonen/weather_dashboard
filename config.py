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

    # Limit request body size to 1 MB
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB

    SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # Prevent CSRF in cross-site contexts
