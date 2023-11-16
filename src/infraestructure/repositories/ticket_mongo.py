from ...domain.dao.ticket import TicketDAO
from ...utils.ErrorHandler import ID_NOT_FOUND
from ..InfraestructureError import InfraestructureError
from .mongo import Mongo, MongoDTO


class Ticket:
    _name = "ticket"
    _pk = "ticket_id"
    _fields = TicketDAO.getFields()

    def __init__(self, chain_connection: None | MongoDTO = None):
        self._r = (
            Mongo.setToDefault()
            if chain_connection is None
            else Mongo(chain_connection)
        )

    def entityExists(self, identifier) -> None | InfraestructureError:
        if self._r.getByID(self._name, self._pk, identifier, self._pk) is None:
            raise InfraestructureError(ID_NOT_FOUND, "Ticket doesnt exists")

    def fetch(self) -> list:
        return self._r.fetch(self._name, self._fields)

    def getByID(self, identity) -> list:
        return self._r.getByID(self._name, self._pk, identity, self._fields)

    def delete(self, identity) -> bool:
        self._r.delete(self._name, self._pk, identity)
        return True

    def create(self, data) -> bool:
        self._r.create(self._name, data)
        return True

    def update(self, data) -> bool:
        self._r.update(self._name, self._pk, data[self._pk], data)
        return True
