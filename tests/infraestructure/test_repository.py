from src.infrastructure.config import Config
from src.infrastructure.mongo.mongo import mongo_interface_test


def test_mongo():
    my_config = Config()
    mongo_interface_test(my_config.MONGO_SERVER)
