from flask import current_app

from typing import Union, Dict, Any, List

from supertokens_python.recipe.emailpassword.interfaces import SignInPostWrongCredentialsError, \
    SignUpPostEmailAlreadyExistsError
from supertokens_python.recipe.thirdpartyemailpassword.interfaces import APIInterface, ThirdPartyAPIOptions, \
    EmailPasswordAPIOptions, ThirdPartySignInUpPostOkResult, EmailPasswordSignInPostOkResult, \
    EmailPasswordSignUpPostOkResult
from supertokens_python.recipe.thirdparty.provider import Provider
from supertokens_python.recipe.emailpassword.types import FormField
from supertokens_python.types import GeneralErrorResponse

from markerr.models.user import User
from markerr.views.users import SignupForm


def override_thirdpartyemailpassword_apis(original_implementation: APIInterface):
    """
    Overrides functions that handle signin/up interactions with the supertokens core.
    The overridden functions insert users into our own database and also change the
    response structure to return additional fields.
    Form validation is a bit messy - if less or more fields are provided, supertokens
    issues messages. If fields are problematic (e.g. non-unique username), WTForms
    issues messages. This means we violate our standard response shape.

    https://supertokens.com/docs/thirdpartyemailpassword/advanced-customizations/apis-override/about

    :param original_implementation:
    :return: original_implementation with overridden functions
    """
    original_thirdparty_sign_in_up_post = original_implementation.thirdparty_sign_in_up_post
    original_emailpassword_sign_in_post = original_implementation.emailpassword_sign_in_post
    original_emailpassword_sign_up_post = original_implementation.emailpassword_sign_up_post

    async def thirdparty_sign_in_up_post(provider: Provider, code: str, redirect_uri: str, client_id: Union[str, None],
                                         auth_code_response: Union[Dict[str, Any], None],
                                         api_options: ThirdPartyAPIOptions, user_context: Dict[str, Any]):
        # TODO Third party integrations
        result = await original_thirdparty_sign_in_up_post(provider, code, redirect_uri, client_id, auth_code_response,
                                                           api_options, user_context)

        if isinstance(result, ThirdPartySignInUpPostOkResult):
            if result.created_new_user:
                pass
            else:
                pass

        return result

    async def emailpassword_sign_in_post(form_fields: List[FormField],
                                         api_options: EmailPasswordAPIOptions, user_context: Dict[str, Any]):
        # call the default behaviour as show below
        result = await original_emailpassword_sign_in_post(form_fields, api_options, user_context)

        if isinstance(result, EmailPasswordSignInPostOkResult):
            # send custom response
            api_options.response.set_status_code(200)
            user = User.query.filter(User.supertoken_id == result.user.user_id).first()
            api_options.response.set_json_content({"status": "success", "data": {"user": user.serialize}})
        elif isinstance(result, SignInPostWrongCredentialsError):
            api_options.response.set_status_code(400)
            api_options.response.set_json_content({"status": "fail", "data": None, "message": "Wrong credentials"})
        # this return doesn't matter. But we must do it
        # cause the function signature expects a response.
        return result

    async def emailpassword_sign_up_post(form_fields: List[FormField],
                                         api_options: EmailPasswordAPIOptions, user_context: Dict[str, Any]):
        # convert the form fields into dict and validate
        signup_form = {}
        for field in form_fields:
            signup_form[field.id] = field.value
        form = SignupForm.from_json(signup_form)
        if not form.validate():
            api_options.response.set_status_code(400)
            api_options.response.set_json_content({"status": "fail", "data": None, "message": form.errors})
            # since default flow hasn't took place yet, we need to return to abort the request
            return GeneralErrorResponse("Invalid form")
        # the default behaviour
        result = await original_emailpassword_sign_up_post(form_fields, api_options, user_context)

        if isinstance(result, EmailPasswordSignUpPostOkResult):
            supertoken_id = result.user.user_id
            email = result.user.email
            # create user
            # we could also use result.user.<field_name>
            user = User(
                email=email,
                supertoken_id=supertoken_id,
                username=form.username.data,
                full_name=form.full_name.data,
                short_name=form.short_name.data
            )
            current_app.session.add(user)
            current_app.session.commit()
            # send response
            api_options.response.set_status_code(200)
            api_options.response.set_json_content({"status": "success", "data": {"user": user.serialize}})
        elif isinstance(result, SignUpPostEmailAlreadyExistsError):
            api_options.response.set_status_code(400)
            api_options.response.set_json_content({"status": "fail", "data": None, "message": "Email already exists"})
        return result

    original_implementation.thirdparty_sign_in_up_post = thirdparty_sign_in_up_post
    original_implementation.emailpassword_sign_in_post = emailpassword_sign_in_post
    original_implementation.emailpassword_sign_up_post = emailpassword_sign_up_post
    return original_implementation
