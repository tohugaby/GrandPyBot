from flask import render_template, request, jsonify

from webapp import app
from webapp.search_manager import SearchConductor
from webapp.sentences_generator import get_random_sentence


@app.route("/")
def index():
    return render_template("webapp/index.html")


@app.route("/process", methods=["POST"])
def process():
    search_terms = ""
    if "search" in request.form:
        search_terms = request.form["search"]
    results = SearchConductor(search_terms).make_full_search()
    return jsonify(dict(results=results))


@app.route("/sentences")
def sentences():
    return jsonify({"sentence": get_random_sentence()})
