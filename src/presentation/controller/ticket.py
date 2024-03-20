from ...application.use_case.ticket import TicketUseCase
from ...domain.model.ticket import TicketDomain
from ...infrastructure.mongo.repositories.ticket_mongo import TicketMongo


class TicketController:
    def __init__(
        self,
        ref_write_uid,
        ref_repository,
        ref_broker,
    ) -> None:
        _w = ref_write_uid
        _r = ref_repository
        _b = ref_broker
        self._uc = TicketUseCase(_w, _r, _b)

    def fetch(self) -> list:
        return self._uc.fetch(0)

    def get_by_id(self, obj_id):
        ticketId = TicketDomain.set_identifier(obj_id)

        return self._uc.get_by_id(ticketId)

    def delete(self, obj_id):
        ticketId = TicketDomain.set_identifier(obj_id)

        return self._uc.delete(ticketId)

    def update(self, obj_id, params: dict):
        ticketId = TicketDomain.set_identifier(obj_id)
        obj = TicketDomain.from_dict(ticketId, params)

        return self._uc.update(obj)

    def create(self, obj_id, where, requirement, because):
        ticketId = TicketDomain.set_identifier(obj_id)
        obj = TicketDomain.new(ticketId, where, requirement, because)

        return self._uc.create(obj)
