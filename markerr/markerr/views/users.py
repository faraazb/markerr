import logging
from flask.views import MethodView
from flask import Blueprint, jsonify, g, current_app
from supertokens_python.recipe.session.framework.flask import verify_session
from supertokens_python.recipe.session import SessionContainer
from wtforms import Form, StringField
from wtforms.validators import InputRequired, ValidationError, Email

from markerr.models.user import User

log = logging.getLogger(__name__)


def unique_username(form, field):
    if User.query.filter(User.username == field.data).first():
        raise ValidationError("Username must be unique")


class SignupForm(Form):
    email = StringField(validators=[InputRequired(), Email(granular_message=True)])
    password = StringField(validators=[InputRequired()])
    username = StringField(validators=[InputRequired(), unique_username])
    full_name = StringField(validators=[InputRequired()])
    short_name = StringField(validators=[InputRequired()])


users = Blueprint("users", __name__, url_prefix="/users")


class Users(MethodView):
    decorators = [verify_session(), users.route("/")]

    def get(self):
        session: SessionContainer = g.supertokens
        supertoken_id = session.get_user_id()
        user = User.query.filter(User.supertoken_id == supertoken_id).first()
        return jsonify({"status": "success", "data": {"user": user.serialize}})
        # if user_id is None:
        #     all_users = User.query.all()
        #     return jsonify({"status": "ok", "user": all_users})
        # user = User.query.filter(id=user_id)
        # if user:
        #     return jsonify({"status": "ok", "user": user})


# @users.route("/", methods=["GET"])
# @verify_session()
# def get_users():
#     session: SessionContainer = g.supertokens
#     user_id = session.get_user_id()
#     log.info(user_id)
#     return jsonify({"id": user_id})

Users.as_view("users")
