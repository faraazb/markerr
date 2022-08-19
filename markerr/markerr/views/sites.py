from flask import Blueprint, render_template

sites = Blueprint("sites", __name__, url_prefix="/sites")


@sites.route("/")
def get():
    return render_template("dashboard.html")
