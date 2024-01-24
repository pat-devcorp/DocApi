import json
import traceback

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
        except PresentationError as p_err:
            response = str(p_err)
            status_code = 422
        except DomainError as d_err:
            response = str(d_err)
            status_code = 500
        except InfrastructureError as i_err:
            response = str(i_err)
            status_code = 500
        except Exception as err:
            error = {
                "message": str(err),
                "traceback": traceback.format_exc(),
            }
            response = str(error)

        finally:
            return json.dumps({"data": response, "statusCode": status_code})

    return wrapper
