from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.my_mongo.mongo import mongo_interface_test


def test_mongo():
    my_config = Bootstrap()
    mongo_interface_test(my_config.MONGO_SERVER)
