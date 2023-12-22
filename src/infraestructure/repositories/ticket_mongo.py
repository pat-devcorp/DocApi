from ...domain.dao.ticket import TicketDAO
from ...utils.ResponseHandler import ID_NOT_FOUND
from ..InfraestructureError import InfraestructureError
from .mongo import Mongo, MongoDTO


class TicketMongo:
    _name = "ticket"
    _pk = "ticketId"
    _fields = TicketDAO.getFields()

    def __init__(self, ref_mongodto: None | MongoDTO = None):
        self._mongo = (
            Mongo.setToDefault() if ref_mongodto is None else Mongo(ref_mongodto)
        )

    def entityExists(self, identifier) -> None | InfraestructureError:
        if self._mongo.getByID(self._name, self._pk, identifier, [self._pk]) is None:
            raise InfraestructureError(ID_NOT_FOUND, "Ticket doesnt exists")

    def fetch(self, fields=None) -> list:
        return self._mongo.fetch(self._name, self._pk, fields or self._fields)

    def getByID(self, identity, fields=None) -> list:
        return self._mongo.getByID(
            self._name, self._pk, identity, fields or self._fields
        )

    def delete(self, identity) -> bool:
        self._mongo.delete(self._name, self._pk, identity)
        return True

    def create(self, data) -> bool:
        self._mongo.create(self._name, self._pk, data)
        return True

    def update(self, data) -> bool:
        self._mongo.update(self._name, self._pk, data[self._pk], data)
        return True
