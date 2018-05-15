from flask_testing import TestCase

from webapp import app, db, FiletoDbHandler


class TestIndexView(TestCase):
    render_templates = False

    def create_app(self):
        # app = webapp.app
        app.config.from_object("config.TestConfig")
        return app

    def test_success(self):
        self.assert200(self.client.get('/', follow_redirects=True))

    def test_assert_template_used(self):
        self.client.get("/", follow_redirects=True)
        self.assert_template_used("webapp/index.html")


class TestProcessView(TestCase):
    render_templates = False

    def create_app(self):
        # app = webapp.app
        app.config.from_object("config.TestConfig")
        return app

    def setUp(self):
        self.in_string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms à Paris ?"
        db.create_all()
        for key in app.config["DATA_LOAD_CONFIG"].keys():
            FiletoDbHandler(db, key)()

    def test_success(self):
        self.assert200(self.client.post("/process", follow_redirects=True, data=dict(test="text de test")))

    def test_return_data(self):
        request = self.client.post("/process", follow_redirects=True, data=dict(search="text de test"))
        for r in request.response:
            self.assertIsInstance(r, bytes)
