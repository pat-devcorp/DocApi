from flask import abort, jsonify, request

# import requests
# from ..config import Config


def isValidUserID(user_id):
    # my_config = Config()
    # payload = {"user_id": user_id}
    # r = requests.get(my_config.USER_API, params=payload)
    # return True if r.status_code == 200 else False
    return True


class UserIDValidator:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        with self.app.app_context():
            write_uid = environ.get('write_uid')
            try:
                if not write_uid:
                    error_message = {'message': 'Missing write_uid parameter'}
                    status_code = 400
                    response = jsonify(error_message)
                    response.update({'status_code': status_code})
                    start_response('400 BAD REQUEST', [('Content-Type', 'application/json')])
                    return response.encode()

                return self.app(environ, start_response)
            except Exception as e:
                error_message = {'message': str(e)}
                status_code = 500
                response = jsonify(error_message)
                response.update({'status_code': status_code})
                start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'application/json')])
                return response.encode()