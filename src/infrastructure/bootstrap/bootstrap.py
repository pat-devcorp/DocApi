import os

from ..broker.rabbitmq import RabbitmqClient, RabbitmqServer
from ..mongo.mongo import MongoClient, MongoServer


class Bootstrap:
    def __init__(self):
        self.get_paths()
        self.get_from_environment()

    def get_paths(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, "..", ".."))
        self.ROUTE_PATH = os.path.join(self.PROJECT_PATH, "rest", "route")
        self.LOG_PATH = os.path.join(self.PROJECT_PATH, "log", "api", "api.log")
        self.BROKER_PATH = os.path.join(self.PROJECT_PATH, "log", "broker")
        self.IMAGE_PATH = os.path.join(self.PROJECT_PATH, "media", "img")
        self.LOG_CONFIG = os.path.join(
            self.PROJECT_PATH, "infrastructure", "logger", "config.json"
        )
        self.BROKER_LOST_MESSAGE_PATH = os.path.join(
            self.PROJECT_PATH, "log", "broker", "lost"
        )

    def get_from_environment(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "BatmanIsBruceWayne")
        self.IS_IN_PRODUCTION = os.getenv("IS_IN_PRODUCTION", 0)

        self.BROKER = os.getenv("BROKER", False)
        if self.BROKER == "RABBITMQ":
            self.RABBITMQ_SERVER = RabbitmqServer(
                hostname=os.environ["RABBITMQ_HOST"],
                port=int(os.environ["RABBITMQ_PORT"]),
                username=os.environ["RABBITMQ_USER"],
                password=os.environ["RABBITMQ_PASS"],
            )
            self.BROKER_RABBITMQ = RabbitmqClient(self.RABBITMQ_SERVER)
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
            self.REPOSITORY_MONGO = MongoClient(self.MONGO_SERVER)
