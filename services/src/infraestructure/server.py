import importlib.util
import os

from flask import Flask

from .config import Config
from .middleware.exceptionHandler import \
    ExceptionHandler as ExceptionHandlerMiddleware


def register_blueprints(app, blueprints):
    for route in blueprints:
        module = importlib.import_module("src.presentation.routes." + route)
        app.register_blueprint(getattr(module, route.split(".")[-1]))


def get_blueprints(directory: str, predicate: str = "") -> list:
    routes = []
    for route in os.listdir(directory):
        if not (route.startswith("__") or route == "src"):
            if route.endswith(".py"):
                routes.append(predicate + route.split(".")[0])
            else:
                routes = routes + get_blueprints(directory + "\\" + route, route + ".")
    return routes


def create_server():
    app = Flask(__name__)
    my_config = Config()
    app.config.from_object(my_config)
    # Import all the blueprints dynamically.
    blueprints = get_blueprints("src/presentation/routes")
    # Register the blueprints with the app.
    register_blueprints(app, blueprints)
    # Add the exception middleware to the app
    app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)
    return app
