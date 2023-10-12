import importlib.util
from pathlib import Path

from flask import Flask

from .config import Config
from .middleware.ExceptionHandler import ExceptionHandler as ExceptionHandlerMiddleware

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app


def registerBlueprints(app, path_ref: Path, blueprints: list):
    local_path = ".".join(path_ref.parts)
    for route in blueprints:
        module_name = f"{local_path}.{route}"
        module = importlib.import_module(module_name)
        app.register_blueprint(getattr(module, route.split(".")[-1]))


def getBlueprints(path_ref: Path, predicate: str = "") -> list:
    blueprints = []
    for item_path in path_ref.iterdir():
        if not (item_path.name.startswith("__") or item_path.suffix == ".http"):
            if item_path.is_file() and item_path.suffix == ".py":
                blueprints.append(predicate + item_path.stem)
            elif item_path.is_dir():
                blueprints.extend(getBlueprints(item_path, item_path.name + "."))
    return blueprints


def createServer():
    app = Flask(__name__)
    my_config = Config()
    app.config.from_object(my_config)
    # Import all the blueprints dynamically.
    blueprint_path = Path("src/presentation/route")
    blueprints = getBlueprints(blueprint_path)
    # Add the exception middleware to the app
    app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)
    registerBlueprints(app, blueprint_path, blueprints)
    # Add prometheus wsgi middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    return app
