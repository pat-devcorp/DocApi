from datetime import datetime
from typing import Dict, List, Protocol

from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient as MongoProvider

from ...utils.status_code import DB_CREATE_FAIL, DB_DELETE_FAIL, DB_UPDATE_FAIL
from ..InfrastructureError import InfrastructureError


class MongoServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    collection: str


class CriteriaProtocol(Protocol):
    clauses: list


class MongoClient:
    def __init__(self, ref_mongo_server: MongoServer):
        self.server = ref_mongo_server
        self.client = None
        self.collection = None

    def set_tablename(self, tablename):
        self.tablename = tablename

    @property
    def dsn(self):
        return f"mongodb://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}"

    def decoder_criteria(matching) -> None:
        print(matching)

    def _connect(self):
        if self.client is None:
            self.client = MongoProvider(self.dsn)
            self.collection = self.client[self.server.collection][
                self.tablename
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

    def fetch(
        self, attrs: List[str] = None, matching: CriteriaProtocol = None
    ) -> List[Dict] | InfrastructureError:
        if matching is not None:
            self.decoder_criteria(matching.clauses)
        attributes = dict
        if attrs is not None:
            attributes = {attr: 1 for attr in attrs}
        return list(self.cursor.find({}, attributes))

    def get_by_id(
        self, identifier: str, attrs: List[str]
    ) -> Dict | None | InfrastructureError:
        attributes = dict
        if attrs is not None:
            attributes = {attr: 1 for attr in attrs}
        return self.cursor.find_one({"_id": identifier}, attributes)

    def delete(self, identifier: str) -> None | InfrastructureError:
        try:
            self.cursor.delete_one({"_id": identifier})
        except Exception as err:
            raise InfrastructureError(DB_DELETE_FAIL, str(err))

    def update(self, identifier: str, kwargs: dict) -> None | InfrastructureError:
        try:
            result = self.cursor.update_one({"_id": identifier}, {"$set": kwargs})
            return result.modified_count
        except Exception as err:
            raise InfrastructureError(DB_UPDATE_FAIL, str(err))

    def create(self, kwargs: dict) -> str | InfrastructureError:
        try:
            identity = self.cursor.insert_one(kwargs).inserted_id
            if isinstance(identity, ObjectId):
                return str(identity)
            return identity
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))

    def insert_many(self, dataset: list[dict]) -> None | InfrastructureError:
        try:
            self.cursor.insert_many(dataset)
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))

    @staticmethod
    def get_object_id():
        now = datetime.now()
        return str(ObjectId.from_datetime(now))


# Test
def mongo_interface_test(ref_mongo_server):
    mongo_repository = MongoClient(ref_mongo_server)
    mongo_repository.set_tablename("test")
    assert hasattr(mongo_repository, "dsn")

    current_id = MongoClient.get_object_id()

    dto = {
        "_id": current_id,
        "write_uid": "0000",
        "requirement": "This is requirement",
    }
    mongo_repository.create(dto)

    data = mongo_repository.fetch(dto.keys())
    print(f"ID: {current_id}")
    print(f"DATA: {data}")
    assert data

    text = "It was modified"
    mongo_repository.update(current_id, {"requirement": text})

    item = mongo_repository.get_by_id(current_id, ["requirement"])
    print(f"ITEM: {item}")
    assert item["requirement"] == text

    mongo_repository.delete(current_id)
    assert mongo_repository.get_by_id(current_id, ["requirement"]) is None

    mongo_repository.insert_many(
        [
            {
                "write_uid": "1111",
                "requirement": "This is requirement 1",
            },
            {
                "write_uid": "2222",
                "requirement": "This is requirement 2",
            },
        ]
    )
