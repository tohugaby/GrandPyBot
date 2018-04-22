from flask import Blueprint, render_template, request, jsonify

webapp_blueprint = Blueprint("webapp",
                             __name__,
                             template_folder="templates",
                             static_folder="static"
                             )


@webapp_blueprint.route("/")
def index():
    return render_template("webapp/index.html")


@webapp_blueprint.route("/process", methods=["POST"])
def process():
    search_terms = ""
    if "search" in request.form:
        search_terms = request.form["search"]
    return jsonify(dict(search=search_terms))
