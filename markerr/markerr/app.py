import logging
import os
import sys
from flask import Flask, abort, g, request
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
import wtforms_json
from flask_cors import CORS
from supertokens_python.framework.flask import Middleware as SupertokensMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.recipe.session.syncio import get_session
from markerr.models.user import User

try:
    from greenlet import getcurrent as _get_ident
except ImportError:
    from threading import get_ident as _get_ident

log_format = '%(asctime)s | %(levelname)s: %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
log = logging.getLogger(__name__)


def create_app():
    """
    Application Factory

    Configures cli commands,
    loads prod/dev config,
    sets up instance dir (TODO Let' see if this is needed),
    sets up SuperTokens and CORS (TODO Fix the frontend origin, place it in config)
    connects to the database and
    registers routes.
    """
    app = Flask(__name__, template_folder="templates")

    from markerr.cli import COMMANDS
    for command in COMMANDS:
        app.cli.add_command(command)

    if app.env == "development":
        log.info("using development config")
        # load config.py at app root
        app.config.from_pyfile('config.py', silent=True)
    else:
        log.info("using production config")
        # load all env variables with "FLASK_" prefix
        # the prefix is dropped for config key
        app.config.from_prefixed_env()

    # ensure the instance folder exists
    # this is not used anywhere though :/
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # setup Supertokens and CORS
    from markerr.auth import init_supertokens
    init_supertokens(
        api_domain=app.config["API_DOMAIN"],
        website_domain=app.config["WEBSITE_DOMAIN"],
        st_connection_uri=app.config["SUPERTOKENS_CONNECTION_URI"],
        st_api_key=app.config["SUPERTOKENS_API_KEY"]
    )
    SupertokensMiddleware(app=app)
    CORS(
        app=app,
        origins=app.config["CORS_ORIGINS"],
        supports_credentials=True,
        allow_headers=["Content-Type"] + get_all_cors_headers()
    )

    # database connection
    import markerr.db as db

    engine = db.create_engine(app.config["DATABASE_URL"])
    try:
        connection = engine.connect()
        connection.close()
    except OperationalError as e:
        log.error("cannot connect to the provided database")
        log.error(e)
        sys.exit()
    db.Session.configure(bind=engine)
    # https://stackoverflow.com/questions/35664436/flask-and-sqlalchemy-handling-sessions
    app.session = scoped_session(db.Session, scopefunc=_get_ident)
    # enable querying using model class syntax instead of session
    db.Base.query = app.session.query_property()

    @app.teardown_appcontext
    def remove_session(*args, **kwargs):
        app.session.remove()

    # load user from session
    @app.before_request
    def load_user():
        # https://supertokens.com/docs/thirdpartyemailpassword/common-customizations/sessions/session-verification-in-api/get-session
        # session can be None
        session = get_session(request, session_required=False)
        if session is not None:
            supertoken_id = session.get_user_id()
            g.user = User.query.filter(User.supertoken_id == supertoken_id).first()
        else:
            g.user = None

    # patches WTForms to support JSON
    wtforms_json.init()

    # register routes
    from markerr.views import users, comments, sites, pages
    blueprints = [
        users.users,
        comments.comments,
        sites.sites,
        pages.pages
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # if this is not there,
    # then OPTIONS requests for the APIs exposed by
    # the supertokens' Middleware will return a 404
    @app.route('/', defaults={'u_path': ''})
    @app.route('/<path:u_path>')
    def catch_all(u_path: str):
        abort(404)

    @app.route('/', methods=['GET'])
    def health():
        return 'OK'

    # TODO There is another method of verifying sessions, check docs
    # @app.route("/test123", methods=["GET"])
    # @verify_session()
    # def test_route():
    #     session: SessionContainer = g.supertokens
    #     user_id = session.get_user_id()
    #     log.info(user_id)
    #     return user_id

    return app
