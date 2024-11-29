from flask import Blueprint, request, render_template, g, redirect, url_for

bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def index():
    return "huanri"

@bp.route("/public_question")
def public_question():
    return "This is the public question page."

@bp.route('/search')
def search():
    return "one"
