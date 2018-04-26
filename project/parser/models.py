from flask_sqlalchemy import SQLAlchemy

from project import app

db = SQLAlchemy(app)


class WordType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(200), nullable=False)
    word_type = db.relationship("Word", backref="word_type", lazy=True)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("word_type.id"), nullable=False)
