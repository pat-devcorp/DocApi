from ..my_logger.my_logger import LogLevel, setup_logging
from ..my_mongo.my_mongo import MongoServer, MyMongoClient
from ..my_rabbitmq.my_rabbitmq import MyRabbitmqClient, RabbitmqServer
from .env import Environment


class App:
    Env: Environment
    MyMongo: MyMongoClient
    MyRabbitmq: MyRabbitmqClient

    def __init__(self):
        self.Env = Environment()

        if self.Env.RabbitmqHost:
            rabbitmqServer = RabbitmqServer(
                hostname=self.Env.RabbitmqHost,
                port=self.Env.RabbitmqPort,
                username=self.Env.RabbitmqUser,
                password=self.Env.RabbitmqPassword,
            )
            self.MyRabbitmq = MyRabbitmqClient(rabbitmqServer)

        if self.Env.MongoHost:
            mongoServer = MongoServer(
                hostname=self.Env.MongoHost,
                port=self.Env.MongoPort,
                username=self.Env.MongoUser,
                password=self.Env.MongoPassword,
                collection=self.Env.MongoDatabase,
            )
            self.MyMongo = MyMongoClient(mongoServer)

        setup_logging(LogLevel.DEBUG if self.Env.IsInProduction else LogLevel.INFO)
