from flask_sqlalchemy import SQLAlchemy
from .views import app

db = SQLAlchemy(app)