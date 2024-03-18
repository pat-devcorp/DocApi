from typing import Dict, List, Protocol

from pydantic import BaseModel
from pymongo import MongoClient

from ...utils.response_code import DB_CREATE_FAIL, DB_DELETE_FAIL, DB_UPDATE_FAIL
from ..InfrastructureError import InfrastructureError


class MongoConfig(Protocol):
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str


class MongoServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    collection: str
    tablename: str
    pk: str


class CriteriaProtocol(Protocol):
    clauses: list


class Mongo:
    def __init__(self, ref_mongo_server: MongoServer):
        self.server = ref_mongo_server
        self.pk = ref_mongo_server.pk
        self.client = None
        self.collection = None

    @property
    def dsn(self):
        return f"mongodb://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}"

    def decoder_criteria(matching) -> None:
        pass

    def _connect(self):
        if self.client is None:
            self.client = MongoClient(self.dsn)
            self.collection = self.client[self.server.collection][
                self.server.tablename
            ]  # Access collection directly

    @property
    def cursor(self):
        self._connect()
        return self.collection  # Use collection as cursor

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            self.client = None

    @classmethod
    def set_default(cls, my_config: MongoConfig, tablename: str, pk: str):
        con = MongoServer(
            hostname=my_config.MONGO_HOST,
            port=my_config.MONGO_PORT,
            username=my_config.MONGO_USER,
            password=my_config.MONGO_PASS,
            collection=my_config.MONGO_DB,
            tablename=tablename,
            pk=pk,
        )
        return cls(con)

    def fetch(
        self, attrs: List[str], matching: CriteriaProtocol
    ) -> List[Dict] | InfrastructureError:
        self.decoder_criteria(matching.clauses)
        data = list(self.cursor.find({}, {attr: 1 for attr in attrs}))
        for item in data:
            item[self.pk] = item.pop("_id")
        return data

    def get_by_id(
        self, identifier: str, attrs: List[str]
    ) -> Dict | None | InfrastructureError:
        item = self.cursor.find_one({"_id": identifier}, {attr: 1 for attr in attrs})
        if item:
            item[self.pk] = item.pop("_id")
        return item

    def delete(self, identifier: str) -> None | InfrastructureError:
        try:
            self.cursor.delete_one({"_id": identifier})
        except Exception as err:
            raise InfrastructureError(DB_DELETE_FAIL, str(err))

    def update(self, identifier: str, kwargs: dict) -> None | InfrastructureError:
        try:
            kwargs.pop(self.pk)
            self.cursor.update_one({"_id": identifier}, {"$set": kwargs})
        except Exception as err:
            raise InfrastructureError(DB_UPDATE_FAIL, str(err))

    def create(self, kwargs: dict) -> None | InfrastructureError:
        try:
            kwargs["_id"] = kwargs.pop(self.pk)
            self.cursor.insert_one(kwargs)
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))


# Test
def mongo_interface_test(my_config):
    mongo_repository = Mongo.set_default(my_config, "test", "identifier")
    print(f"CONNECTION: {mongo_repository.dsn}")

    current_id = "87378a1e-894c-11ee-b9d1-0242ac120002"
    dto = {
        "writeUId": "8888",
        "identifier": current_id,
        "requirement": "This is requirement",
    }
    mongo_repository.create(dto)

    data = mongo_repository.fetch(dto.keys(), list())
    assert data

    text = "It was modified"
    mongo_repository.update(current_id, {"requirement": text})

    item = mongo_repository.get_by_id(current_id, ["requirement"])
    assert item["requirement"] == text

    mongo_repository.delete(current_id)
    assert mongo_repository.get_by_id(current_id, ["requirement"]) is None
