import logging

from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from ..infrastructure.bootstrap.bootstrap import Bootstrap
from ..infrastructure.logger.logger import setup_logging
from .route import download_file, hello, image, person, ticket


def register_blueprints(app):
    app.register_blueprint(download_file.download_file_route)
    app.register_blueprint(hello.hello_route)
    app.register_blueprint(image.image_route)
    app.register_blueprint(person.person_route)
    app.register_blueprint(ticket.ticket_route)


def create_server():
    app = Flask(__name__)

    my_config = Bootstrap()
    app.config.from_object(my_config)
    print("---CONFIG")
    print(vars(my_config))

    register_blueprints(app)

    if my_config.IS_IN_PRODUCTION:
        logging.getLogger("rest_app")
        setup_logging(my_config.LOG_CONFIG)
        logging.basicConfig(level="INFO")

    # Add prometheus wsgi middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
    return app
