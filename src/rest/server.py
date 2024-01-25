import importlib.util
from pathlib import Path

from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from ..infrastructure.config import Config
from ..infrastructure.logger import set_format_to_json


def register_blueprints(app, path_ref: Path, blueprints: list):
    local_path = ".".join(path_ref.parts)
    for route in blueprints:
        module_name = f"{local_path}.{route}"
        module = importlib.import_module(module_name)
        app.register_blueprint(getattr(module, route.split(".")[-1]))


def get_blueprints(path_ref: Path, predicate: str = "") -> list:
    blueprints = []
    for item_path in path_ref.iterdir():
        if not (item_path.name.startswith("__") or item_path.suffix == ".http"):
            if item_path.is_file() and item_path.suffix == ".py":
                blueprints.append(predicate + item_path.stem)
            elif item_path.is_dir():
                blueprints.extend(get_blueprints(item_path, item_path.name + "."))
    return blueprints


def create_server():
    app = Flask(__name__)

    my_config = Config()
    app.config.from_object(my_config)
    print("---CONFIG")
    print(vars(my_config))

    blueprint_path = Path(my_config.ROUTE_PATH)
    blueprints = get_blueprints(blueprint_path)
    register_blueprints(app, blueprint_path, blueprints)
    print("---ROUTES")
    print(blueprints)

    if my_config.IS_IN_PRODUCTION:
        set_format_to_json(my_config.LOG_PATH)

    # Add prometheus wsgi middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
    return app
