import os

from ..broker.rabbitmq import RabbitmqServer
from ..mongo.mongo import MongoServer


class Bootstrap:
    def __init__(self):
        self.get_paths()
        self.get_from_environment()

    def get_paths(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, ".."))
        self.ROUTE_PATH = os.path.join("src", "rest", "route")
        self.LOG_PATH = os.path.join("src", "log", "api", "api.log")
        self.BROKER_PATH = os.path.join("src", "log", "broker")
        self.IMAGE_FOLDER = os.path.join("src", "media", "img")
        self.LOG_CONFIG = os.path.join(
            self.PROJECT_PATH, "infrastructure", "logger", "config.json"
        )

    def get_from_environment(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "BatmanIsBruceWayne")
        self.IS_IN_PRODUCTION = os.getenv("IS_IN_PRODUCTION", 0)

        self.BROKER = os.getenv("BROKER", False)
        self.BROKER_LOST_MESSAGE_PATH = os.getenv(
            "BROKER_LOST_MESSAGE_PATH", os.path.join("src", "log", "broker", "lost")
        )
        if self.BROKER == "RABBITMQ":
            self.RABBITMQ_SERVER = RabbitmqServer(
                hostname=os.environ["RABBITMQ_HOST"],
                port=int(os.environ["RABBITMQ_PORT"]),
                username=os.environ["RABBITMQ_USER"],
                password=os.environ["RABBITMQ_PASS"],
            )
        if self.BROKER == "KAFKA":
            self.KAFKA_HOST = os.environ["KAFKA_HOST"]
            self.KAFKA_PORT = os.environ["KAFKA_PORT"]

        self.DB = os.getenv("DB", False)
        if self.DB == "MONGO":
            self.MONGO_SERVER = MongoServer(
                hostname=os.environ["MONGO_HOST"],
                port=int(os.environ["MONGO_PORT"]),
                username=os.environ["MONGO_USER"],
                password=os.environ["MONGO_PASS"],
                collection=os.environ["MONGO_DB"],
            )
