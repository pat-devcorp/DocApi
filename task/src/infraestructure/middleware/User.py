import requests
from flask import abort, request

from ..config import Config


def validateIdentity(user_id):
    my_config = Config()
    payload = {"user_id": user_id}
    r = requests.get(my_config.USER_API, params=payload)
    return True if r.status_code == 200 else False


# Custom middleware function
def validate_user_id_middleware():
    def middleware(wsgi_app):
        def wrapped(environ, start_response):
            user_id = request.args.get("write_uid")

            if user_id is not None:
                validateIdentity(user_id)
                print(f"Token ID: {user_id}")
            else:
                # 'token_id' is not present in the request, you can return an error response or abort
                abort(401, "Token ID is missing from the request.")

            return wsgi_app(environ, start_response)

        return wrapped

    return middleware
