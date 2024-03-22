from infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.mongo.mongo import mongo_interface_test


def test_mongo():
    my_config = Bootstrap()
    mongo_interface_test(my_config.MONGO_SERVER)
