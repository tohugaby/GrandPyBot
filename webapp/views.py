from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    search_terms = ""
    if "search" in request.form:
        search_terms = request.form["search"]
    return jsonify(dict(search=search_terms))
