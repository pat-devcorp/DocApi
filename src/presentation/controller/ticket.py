from ...application.use_case.ticket import TicketUseCase
from ...domain.enum.channel_type import ChannelType
from ...domain.enum.ticket_state import TicketState
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
        _r = TicketMongo(ref_repository)
        _b = ref_broker
        self._uc = TicketUseCase(_w, _r, _b)

    def fetch(self) -> list:
        return self._uc.fetch(0)

    def get_by_id(self, ticket_id):
        ticket_id = TicketDomain.set_identifier(ticket_id)

        return self._uc.get_by_id(ticket_id)

    def delete(self, ticket_id):
        ticket_id = TicketDomain.set_identifier(ticket_id)

        return self._uc.delete(ticket_id)

    def update(self, ticket_id, params: dict):
        ticket_id = TicketDomain.set_identifier(ticket_id)
        obj = TicketDomain.from_dict(ticket_id, params)

        return self._uc.update(obj)

    def create(
        self,
        ticket_id,
        channel_type,
        requirement,
        because,
        state=None,
        attrs: dict = None,
    ):
        ticket_id = TicketDomain.set_identifier(ticket_id)
        enum_channel = ChannelType(channel_type)
        enum_state = None
        if state is None:
            enum_state = TicketState.CREATED
        if attrs is None:
            attrs = {}
        obj = TicketDomain.new(
            ticket_id, enum_channel, requirement, because, enum_state, attrs
        )

        return self._uc.create(obj)
