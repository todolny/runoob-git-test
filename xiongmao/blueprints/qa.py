from flask import Blueprint, render_template

bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def index():
    return "huanri"

@bp.route("/public_question")
def public_question():
    return "This is the public question page."
