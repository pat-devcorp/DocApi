from ...InfrastructureError import InfrastructureError
from ..mongo import MongoClient


class TicketMongo:
    tablename = "ticket"

    def __init__(self, ref_client: MongoClient, pk=None) -> None | InfrastructureError:
        self._m = ref_client
        self._m.set_tablename(self.tablename)
        self.pk = pk if pk is not None else "_id"

    def entity_exists(self, identifier) -> bool:
        if self._m.get_by_id(identifier, [self._pk]) is None:
            return False
        return True

    def fetch(self, fields: list, matching) -> list:
        dataset = self._m.fetch(fields, matching)
        if self.pk != "_id":
            for item in dataset:
                item[self.pk] = item.pop("_id")
        return dataset

    def get_by_id(self, identifier, fields: list) -> dict:
        item = self._m.get_by_id(identifier, fields)
        if self.pk != "_id" and item:
            item[self.pk] = item.pop("_id")
        return item

    def delete(self, identifier) -> None | InfrastructureError:
        self._m.delete(identifier)
        return None

    def update(self, identifier, item) -> None | InfrastructureError:
        item.pop(self.pk)
        self._m.update(identifier, item)
        return None

    def create(self, item) -> None | InfrastructureError:
        item["_id"] = item.pop(self.pk)
        self._m.create(item)
        return None

    def insert_many(self, data):
        dataset = list(data)
        for item in dataset:
            item["_id"] = item.pop(self.pk)
        self._m.insert_many(dataset)
        return None
