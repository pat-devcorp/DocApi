import json
import traceback

from src.application.application_error import ApplicationError
from src.application.infrastructure_error import InfrastructureError
from src.domain.domain_error import DomainError
from src.presentation.presentation_error import PresentationError


def exception_handler(func):
    def wrapper(*args, **kwargs):
        response = ""
        status_code = 200

        try:
            response = func(*args, **kwargs) or "OK"
        except PresentationError as p_err:
            response = str(p_err)
            status_code = 100
        except DomainError as d_err:
            response = str(d_err)
            status_code = 200
        except ApplicationError as a_err:
            response = str(a_err)
            status_code = 300
        except InfrastructureError as i_err:
            response = str(i_err)
            status_code = 400
        except TimeoutError as t_err:
            response = str(t_err)
            status_code = 500
        except Exception as err:
            error = {
                "message": str(err),
                "traceback": traceback.format_exc(),
            }
            response = str(error)
            status_code = 600

        finally:
            return json.dumps({"data": response, "statusCode": status_code})

    # Renaming the function name:
    wrapper.__name__ = func.__name__

    return wrapper
