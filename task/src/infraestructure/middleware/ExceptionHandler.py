import traceback

from flask import jsonify

from ...application.ApplicationError import ApplicationError
from ...domain.DomainError import DomainError
from ...presentation.PresentationError import PresentationError
from ...utils.HandlerError import HandlerError
from ..InfraestructureError import InfraestructureError


class ExceptionHandler:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = dict()
        status_code = 403
        try:
            return self.app(environ, start_response)
        except HandlerError as he:
            response = jsonify(he)
            status_code = 400
        except PresentationError as ce:
            response = jsonify(ce)
            status_code = 422
        except ApplicationError as ae:
            response = jsonify(ae)
            status_code = 409
        except DomainError as de:
            response = jsonify(de)
            status_code = 500
        except InfraestructureError as fe:
            response = jsonify(fe)
            status_code = 500
        except Exception as e:
            error = {
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            response = jsonify(error)
        finally:
            response.update({"status_code": status_code})
