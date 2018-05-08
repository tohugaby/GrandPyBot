from flask import Flask, redirect, url_for

from project.webapp.views import webapp_blueprint

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(webapp_blueprint, url_prefix="/webapp")


@app.route("/")
def root():
    return redirect(url_for("webapp.index"))
