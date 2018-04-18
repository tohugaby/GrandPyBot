from flask_testing import TestCase

import webapp


class TestIndexView(TestCase):
    render_templates = False

    def create_app(self):
        app = webapp.app
        app.config["TESTING"] = True
        return app

    def test_success(self):
        self.assert200(self.client.get('/'))

    def test_assert_template_used(self):
        self.client.get("/")
        self.assert_template_used("index.html")


class TestProcessView(TestCase):
    render_templates = False

    def create_app(self):
        app = webapp.app
        app.config["TESTING"] = True
        return app

    def test_success(self):
        self.assert200(self.client.post("/process", data=dict(test="text de test")))

    def test_return_data(self):
        request = self.client.post("/process", data=dict(search="text de test"))
        for r in request.response:
            print(r)
            self.assertIsInstance(r, bytes)
