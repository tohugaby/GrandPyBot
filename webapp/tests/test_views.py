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
