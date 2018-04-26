from flask_testing import TestCase

from project import app
from project.parser.models import db, WordType, Word
from project.parser.word_files_handler.initial_data_handlers import FiletoDbHandler


class TestDataLoading(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def protocol(self, db, key):
        FiletoDbHandler(db, key)()
        q = db.session.query(WordType)
        self.assertGreater(q.count(), 0)
        q2 = q.filter(WordType.type_name == key)
        self.assertEqual(q2.count(), 1)
        q3 = db.session.query(Word)
        self.assertGreater(q3.count(), 0)

    def test_load_to_db_stop_words(self):
        key = "stop_words"
        self.protocol(db, key)

    def test_load_to_db_french_words(self):
        key = "french_words"
        self.protocol(db, key)

    def test_load_to_db_cities(self):
        key = "cities"
        self.protocol(db, key)

    def test_load_to_db_countries(self):
        key = "countries"
        self.protocol(db, key)
