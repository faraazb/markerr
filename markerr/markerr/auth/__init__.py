import logging

from supertokens_python import SupertokensConfig
from supertokens_python.recipe import session
from supertokens_python import init, InputAppInfo
from supertokens_python.recipe import thirdpartyemailpassword
from supertokens_python.recipe.emailpassword import InputFormField

from markerr.auth.error_handlers import InputErrorHandlers
from markerr.auth.supertoken_apis_override import override_thirdpartyemailpassword_apis

log = logging.getLogger(__name__)


def init_supertokens(api_domain, website_domain, st_connection_uri, st_api_key=None):
    init(
        app_info=InputAppInfo(
            app_name="Annotator",
            api_domain=api_domain,
            website_domain=website_domain,
            api_base_path="/auth",
            website_base_path="/auth"
        ),
        supertokens_config=SupertokensConfig(
            # These are the connection details of the app you created on supertokens.com
            connection_uri=st_connection_uri,
            api_key=st_api_key
        ),
        framework='flask',
        recipe_list=[
            # initializes session features
            session.init(
                # allow cross-origin requests (e.g. from example.com to annotator.test)
                # third-party cookies are disabled by default on Safari and Chrome Incognito,
                # instruct user to enable.
                # the problem is every client website needs a separate login/session,
                # using cookie_domain and  an iframe and HTML5 postMessage API to get cookies
                # or get tokens from annotator.test's local storage is a viable solution
                # the below also needs a https api_domain
                cookie_same_site="none",
                # anti_csrf="VIA_TOKEN",
                # jwt=session.JWTConfig(enable=True),
                error_handlers=InputErrorHandlers()
            ),
            thirdpartyemailpassword.init(
                override=thirdpartyemailpassword.InputOverrideConfig(
                    apis=override_thirdpartyemailpassword_apis
                ),
                sign_up_feature=thirdpartyemailpassword.InputSignUpFeature(
                    form_fields=[
                        InputFormField(id='username'),
                        InputFormField(id='full_name'),
                        InputFormField(id='short_name')
                    ]
                )
            )
        ]
    )
