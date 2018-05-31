import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config = os.environ.get('FLASK_CONFIG') or 'config.DevConfig'
app.config.from_object(config)
db = SQLAlchemy(app)
from webapp import routes
from webapp.word_files_handler.initial_data_handlers import FiletoDbHandler


@app.cli.command()
def init_db():
    db.create_all()
    for key in app.config["DATA_LOAD_CONFIG"].keys():
        FiletoDbHandler(db, key)()
