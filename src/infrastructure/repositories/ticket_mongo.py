from ...domain.model.ticket import Ticket
from ...utils.ResponseHandler import id_NOT_FOUND
from ..InfrastructureError import infrastructureError
from .mongo import Mongo, MongoDTO


class TicketMongo:
    _name = "ticket"
    _pk = "ticketId"

    def __init__(self, ref_mongoDto: MongoDTO | None) -> None | infrastructureError:
        self._m = Mongo.setToDefault() if ref_mongoDto is None else Mongo(ref_mongoDto)
        self._fields = Ticket._fields()

    def entityExists(self, identifier) -> None | infrastructureError:
        if self._m.getById(self._name, self._pk, identifier, [self._pk]) is None:
            raise infrastructureError(id_NOT_FOUND, "Ticket does not exists")

    def fetch(self, fields=None) -> list:
        return self._m.fetch(self._name, self._pk, fields or self._fields)

    def getById(self, identifier, fields=None) -> list:
        return self._m.getById(self._name, self._pk, identifier, fields or self._fields)

    def delete(self, identifier) -> None | infrastructureError:
        self._m.delete(self._name, self._pk, identifier)
        return True

    def create(self, data) -> None | infrastructureError:
        self._m.create(self._name, self._pk, data)
        return True

    def update(self, data) -> None | infrastructureError:
        self._m.update(self._name, self._pk, data[self._pk], data)
        return True
