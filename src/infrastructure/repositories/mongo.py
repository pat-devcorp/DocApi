import functools
from typing import Dict, List

from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from pymongo import MongoClient

from ...utils.ResponseHandler import (
    DB_CONNECTION_FAIL,
    DB_CREATE_FAIL,
    DB_DELETE_FAIL,
    DB_UPDATE_FAIL,
)
from ..config import Config
from ..InfrastructureError import InfrastructureError


class MongoServer(BaseModel):
    server: IPvAnyAddress
    port: int
    user: str
    password: str
    collection: str
    tablename: str
    pk: str


def testMongo():
    mongo_repository = Mongo.setDefault("test", "identifier")
    print(f"CONNECTION: {mongo_repository.getDSN}")

    current_id = "87378a1e-894c-11ee-b9d1-0242ac120002"
    dto = {
        "writeUId": "8888",
        "identifier": current_id,
        "description": "This is description",
    }
    mongo_repository.create(dto)

    data = mongo_repository.fetch(dto.keys())
    assert data

    text = "It was modified"
    mongo_repository.update(current_id, {"description": text})

    data = mongo_repository.getById(current_id, ["description"])
    assert data["description"] == text

    mongo_repository.delete(current_id)
    assert mongo_repository.getById(current_id, ["description"]) is None


class Mongo:
    def __init__(self, ref_mongo_server: MongoServer):
        self.mongo_server = ref_mongo_server
        self.connection = None
        self.collection = None
        self.client = None

    @property
    def getDSN(self):
        return (
            f"mongodb://{self.mongo_server.user}:{self.mongo_server.password}@"
            f"{self.mongo_server.server}:{self.mongo_server.port}/?authMechanism=DEFAULT"
        )

    @classmethod
    def setDefault(cls, tablename, pk):
        my_config = Config()
        con = MongoServer(
            server=my_config.MONGO_HOST,
            port=my_config.MONGO_PORT,
            user=my_config.MONGO_USER,
            password=my_config.MONGO_PASSWORD,
            collection=my_config.MONGO_COLLECTION,
            tablename=tablename,
            pk=pk,
        )
        return cls(con)

    def startConnection(self) -> bool | InfrastructureError:
        try:
            self.client = MongoClient(self.getDSN)
            self.connection = self.client[self.mongo_server.collection]
            self.collection = self.collection[self.mongo_server.tablename]
        except Exception as err:
            raise InfrastructureError(
                DB_CONNECTION_FAIL,
                f"{self.getDSN}\n{str(err)}",
            )

    def manage_connection(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.collection or self.client:
                self.startConnection()
            try:
                return func(self, *args, **kwargs)
            finally:
                # Close connection only when necessary (e.g., when encountering errors)
                if self.client and not self.client.is_closed:
                    self.client.close()

        return wrapper

    def fetch(self, attrs: List[str]) -> List[Dict] | InfrastructureError:
        return list(self.collection.find({}, {attr: 1 for attr in attrs}))

    def getByID(
        self, identifier: str, attrs: List[str]
    ) -> Dict | None | InfrastructureError:
        return self.collection.find_one(
            {self.pk: identifier}, {attr: 1 for attr in attrs}
        )

    @manage_connection
    def delete(self, identifier: str):
        try:
            self.collection.delete_one({self.pk: identifier})
        except Exception as err:
            raise InfrastructureError(DB_DELETE_FAIL, str(err))

    @manage_connection
    def update(self, identifier: str, kwargs: dict):
        try:
            self.collection.update_one({self.pk: identifier}, {"$set": kwargs})
        except Exception as err:
            raise InfrastructureError(DB_UPDATE_FAIL, str(err))

    @manage_connection
    def create(self, kwargs: dict):
        try:
            self.collection.insert_one(kwargs)
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))
