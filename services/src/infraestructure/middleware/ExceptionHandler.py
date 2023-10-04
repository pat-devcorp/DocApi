import traceback

from flask import jsonify

from ...application.ApplicationError import ApplicationError
from ...presentation.controller import ControllerError
from ...presentation.interface import InterfaceError
from ...struct.DomainError import DomainError


class ExceptionHandler(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except InterfaceError as ie:
            response = jsonify(ie)
            response.status_code = 400
        except ControllerError as ce:
            response = jsonify(ce)
            response.status_code = 422
        except ApplicationError as ae:
            response = jsonify(ae)
            response.status_code = 409
        except DomainError as de:
            response = jsonify(de)
            response.status_code = 500
        except Exception as e:
            error = {
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            response = jsonify(error)
            response.status_code = 403
            return response(environ, start_response)
