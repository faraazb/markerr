from flask import Blueprint, request, jsonify
from sqlalchemy.exc import MultipleResultsFound
from markerr.models.site import Site

sites = Blueprint("sites", __name__, url_prefix="/sites")


@sites.route("/", methods=["GET"])
def get():
    name = request.args.get("domain")
    try:
        site = Site.query.filter(Site.name == name).one_or_none()
        if site is None:
            return jsonify({"status": "success", "data": None})
        return jsonify({"status": "success", "data": site.serialize})
    except MultipleResultsFound:
        return jsonify({"status": "fail", "message": "Multiple sites found"})

