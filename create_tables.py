# create_tables.py
from weather import create_app, db
import weather.models  # This registers SessionMetric with SQLAlchemy

app = create_app()

with app.app_context():
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("Registered tables:", db.metadata.tables.keys())
    db.create_all()
    print("Tables created successfully!")
