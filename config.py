# config.py

import os

class Config:
    # Use environment variables for sensitive info
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your_dummy_api_key')
    DEBUG = True
    # If using a database, define DATABASE_URI, etc.

