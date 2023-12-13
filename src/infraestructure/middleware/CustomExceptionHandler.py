import traceback

from flask import str

from ...application.ApplicationError import ApplicationError
from ...domain.DomainError import DomainError
from ...presentation.PresentationError import PresentationError
from ...utils.HandlerError import HandlerError
from ..InfraestructureError import InfraestructureError


class CustomExceptionHandler:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = dict()
        status_code = 403

        try:
            print("---WELCOME!")
            return self.app(environ, start_response)
        except HandlerError as he:
            response = str(he)
            status_code = 400
        except PresentationError as ce:
            response = str(ce)
            status_code = 422
        except ApplicationError as ae:
            response = str(ae)
            status_code = 409
        except DomainError as de:
            response = str(de)
            status_code = 500
        except InfraestructureError as fe:
            response = str(fe)
            status_code = 500
        except Exception as e:
            error = {
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            response = str(error)

        finally:
            response.update({"status_code": status_code})
            return response
