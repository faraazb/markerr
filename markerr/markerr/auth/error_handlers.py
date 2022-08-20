from typing import Callable, Awaitable, Union

from supertokens_python.framework import BaseRequest, BaseResponse
from supertokens_python.recipe.session import SessionRecipe
from supertokens_python.recipe.session.cookie_and_header import clear_cookies
from supertokens_python.recipe.session.utils import ErrorHandlers, default_token_theft_detected_callback


class InputErrorHandlers(ErrorHandlers):
    """
    supertokens sdk doesn't allow passing a custom refresh_token callback,
    so this reimplements ``InputErrorHandlers`` to allow us to do just that.

    """
    def __init__(
        self,
        on_token_theft_detected: Union[
            None,
            Callable[
                [BaseRequest, str, str, BaseResponse],
                Union[BaseResponse, Awaitable[BaseResponse]],
            ],
        ] = None,
        on_unauthorised: Union[
            Callable[
                [BaseRequest, str, BaseResponse],
                Union[BaseResponse, Awaitable[BaseResponse]],
            ],
            None,
        ] = None,
        on_try_refresh_token: Union[
            Callable[
                [BaseRequest, str, BaseResponse],
                Union[BaseResponse, Awaitable[BaseResponse]],
            ],
            None,
        ] = None,
    ):
        if on_token_theft_detected is None:
            on_token_theft_detected = default_token_theft_detected_callback
        if on_unauthorised is None:
            on_unauthorised = InputErrorHandlers.unauthorised_callback
        if on_try_refresh_token is None:
            on_try_refresh_token = InputErrorHandlers.try_refresh_token_callback
        super().__init__(
            on_token_theft_detected, on_try_refresh_token, on_unauthorised
        )

    @staticmethod
    async def try_refresh_token_callback(req: BaseRequest, err: str, response: BaseResponse):
        response.set_status_code(401)
        response.set_json_content({"status": "fail", "message": err})
        return response

    @staticmethod
    async def unauthorised_callback(req: BaseRequest, err: str, response: BaseResponse):
        recipe = SessionRecipe.get_instance()
        response.set_status_code(401)
        response.set_json_content({"status": "fail", "message": "unauthorised"})
        clear_cookies(recipe=recipe, response=response)
        return response
