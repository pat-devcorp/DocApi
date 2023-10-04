import importlib.util
import os
from flask import Flask
from pathlib import Path

from .config import Config
from .middleware.ExceptionHandler import ExceptionHandler as ExceptionHandlerMiddleware


def registerBlueprints(app, path_ref: Path, blueprints: list):
    local_path = ".".join(path_ref.parts)
    for route in blueprints:
        module_name = f"{local_path}.{route}"
        module = importlib.import_module(module_name)
        app.register_blueprint(getattr(module, route.split(".")[-1]))


def getBlueprints(path_ref: Path, predicate: str = "") -> list:
    blueprints = []
    for item_path in path_ref.iterdir():
        if not (item_path.name.startswith("__") or item_path.suffix == ".http" or item_path.name == "InterfaceError.py"):
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
    # Register the blueprints with the app.
    registerBlueprints(app, blueprint_path, blueprints)
    # Add the exception middleware to the app
    app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)
    return app
