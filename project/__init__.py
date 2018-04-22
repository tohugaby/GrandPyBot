from flask import Flask, redirect, url_for

app = Flask(__name__)
app.config.from_object('config')
from project.webapp.views import webapp_blueprint

app.register_blueprint(webapp_blueprint, url_prefix="/webapp")


@app.route("/")
def root():
    return redirect(url_for("webapp.index"))
