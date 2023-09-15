import traceback

from flask import jsonify


class ExceptionHandler(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            error = {
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            response = jsonify(error)
            response.status_code = 500
            return response(environ, start_response)
