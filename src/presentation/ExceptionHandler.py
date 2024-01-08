import traceback

from flask import jsonify

from ..domain.DomainError import DomainError
from ..infrastructure.InfrastructureError import InfrastructureError
from ..presentation.PresentationError import PresentationError


def exception_handler(func):
    def wrapper(*args, **kwargs):
        response = ""
        status_code = 403

        try:
            response = func(*args, **kwargs) or "OK"
            status_code = 200
        except PresentationError as ce:
            response = str(ce)
            status_code = 422
        except DomainError as de:
            response = str(de)
            status_code = 500
        except InfrastructureError as fe:
            response = str(fe)
            status_code = 500
        except Exception as e:
            error = {
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            response = str(error)

        finally:
            return jsonify({"data": response, "status_code": status_code})

    return wrapper
