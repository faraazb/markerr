from flask import current_app, request, Blueprint, jsonify
from markerr.models.site import Site, Page
from wtforms import Form, StringField
from wtforms.validators import InputRequired
from supertokens_python.recipe.session.framework.flask import verify_session


class PageForm(Form):
    url = StringField(validators=[InputRequired()])


pages = Blueprint("pages", __name__, url_prefix="/pages")


@pages.route("/<uuid:site_id>", methods=["POST"])
@verify_session()
def post(site_id):
    """
    Create a page of a site
    :param site_id:
    :return: the created page
    """

    site = Site.query.get(site_id)
    if not site:
        return jsonify({"status": "fail", "message": "Invalid site_id. SIte does not exist."}), 400
    form = PageForm.from_json(request.json)
    if not form.validate():
        return jsonify({"status": "fail", "data": form.errors, "message": "Form field errors"}), 400
    page = Page.query.filter(Page.url == form.url.data).one_or_none()
    if page:
        return jsonify({"status": "fail", "message": "Page already exists"}), 400
    page = Page(site_id=site_id, url=form.url.data)
    current_app.session.add(page)
    current_app.session.commit()
    return jsonify({"status": "success", "data": page.serialize}), 200
