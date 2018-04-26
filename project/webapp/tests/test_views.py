from flask_testing import TestCase

from project import app


class TestIndexView(TestCase):
    render_templates = False

    def create_app(self):
        # app = webapp.app
        app.config["TESTING"] = True
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
        app.config["TESTING"] = True
        return app

    def test_success(self):
        self.assert200(self.client.post("/webapp/process", follow_redirects=True, data=dict(test="text de test")))

    def test_return_data(self):
        request = self.client.post("/webapp/process", follow_redirects=True, data=dict(search="text de test"))
        for r in request.response:
            self.assertIsInstance(r, bytes)
