from flask_sqlalchemy import SQLAlchemy

from webapp import app
from webapp.models import db, WordType, Word


class FiletoDbHandler:
    """
    handle word list data to integrate them in Word and WordType table from app db. Database,
    category_name, files to handle and handler are required.
    """

    def __init__(self, database: SQLAlchemy, category, files: list = list(), handler_method: str = None):
        self.database = database
        self.category_name = category
        self.category_instance = self.database.session.query(WordType).filter(WordType.type_name ==
                                                                              self.category_name).first()
        self.files = files
        if not files:
            self.files = app.config["DATA_LOAD_CONFIG"][self.category_name]["files"]
        if handler_method is not None:
            handler = handler_method
        else:
            handler = app.config["DATA_LOAD_CONFIG"][self.category_name]["handler"]
        exec("from .handler_methods import %s" % handler)
        self.data_handler = eval(handler)

    def __call__(self, *args, **kwargs):
        self.add_word_to_db()

    def _add_category_to_db(self):
        if not self.category_instance:
            self.category_instance = WordType(type_name=self.category_name)
            self.database.session.add(self.category_instance)
            self.database.session.commit()

    def add_word_to_db(self):
        self._add_category_to_db()
        data = self.data_handler()
        for word in data:
            db.session.add(Word(word=word, category=self.category_instance.id))

        db.session.flush()
        db.session.commit()
