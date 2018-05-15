"""
Contains all parser db models
"""

from webapp import db


class WordType(db.Model):
    """
    Define all type words stored in database
    """
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(200), nullable=False)
    word_type = db.relationship("Word", backref="word_type", lazy=True)


class Word(db.Model):
    """
    Words stored in database. They are used by parsers.
    """
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("word_type.id"), nullable=False)
