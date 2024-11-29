from dotenv import find_dotenv, load_dotenv
from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.infrastructure.bootstrap.app import App

from .hello import hello_route
from .task import task_route


def register_blueprints(app):
    app.register_blueprint(hello_route)
    app.register_blueprint(task_route)


def create_server():
    load_dotenv(find_dotenv())
    app = Flask(__name__)

    app.myApp = App()
    print(f"---CONFIG: {app.myApp.Env}")
    app.config.from_object(app.myApp.Env)

    register_blueprints(app)

    # Add prometheus wsgi middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
    return app
