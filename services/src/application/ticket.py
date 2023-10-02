from enum import Enum

from ..infraestructure.config import Config
from ..infraestructure.producer import Producer
from ..struct.audit import Audit as AuditDomain
from ..struct.audit import AuditStruct
from ..struct.ticket import StateTicket
from ..struct.ticket import Ticket as TicketDomain
from ..struct.ticket import TicketStruct
from .ApplicationError import applicationError
from .repositoryProtocol import RepositoryProtocol


class EventTicket(Enum):
    CREATED = "C"
    UPDATED = "U"
    DELETED = "D"


class Ticket:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self._fields = TicketStruct._fields + AuditStruct._fields
        self._producer = Producer(Config.PRODUCER_HOST, Config.PRODUCER_PORT)

    def stateMachine(self, write_uid, event: EventTicket, my_ticket: TicketStruct):
        kafka_topic = ""
        message = my_ticket.asDict()

        if event.CREATED:
            self.state = StateTicket.CREATED
            kafka_topic = "TICKET CREATED: {my_ticket.ticket_id}"
            self.create(write_uid, my_ticket)
        if event.DELETED:
            kafka_topic = "TICKET DELETED: {my_ticket.ticket_id}"
            self.delete(write_uid, my_ticket.ticket_id)
        if event.UPDATED:
            kafka_topic = "TICKET UPDATED: {my_ticket.ticket_id}"
            self.update(write_uid, my_ticket.ticket_id, my_ticket)

        self._producer.send_message(kafka_topic, message)

    def ensureTicketId(self, my_ticket: TicketStruct) -> None:
        my_ticket = self.getByID(my_ticket.ticket_id)
        if not my_ticket:
            return None
        return my_ticket

    def getAll(self) -> list:
        return self.my_repository.get(TicketStruct.__name__, self._fields)

    def getByID(self, ticket_id) -> dict:
        return self.my_repository.getByID(
            TicketStruct.__name__, "ticket_id", ticket_id, self._fields
        )

    def create(self, write_uid, ref_dto: dict) -> dict:
        my_audit = AuditDomain.create(write_uid)

        my_dto = {k: v for k, v in ref_dto.items() if k in TicketStruct._fields}
        my_dto.update(my_audit)

        my_ticket_struct = TicketDomain()
        my_ticket_struct.create(**ref_dto)

        self.my_repository.create(TicketStruct.__name__, my_ticket_struct.asDict())

        return my_ticket_struct.asDict()

    def update(self, write_uid, ticket_id, ref_dto: dict) -> dict:
        my_ticket = self.ensureTicketId(ticket_id)
        if not my_ticket:
            raise applicationError(["Ticket does not exist"])

        my_dto_audit = {k: v for k, v in my_ticket if k in AuditStruct._fields}
        my_audit = AuditDomain.update(write_uid, **my_dto_audit)

        self.my_repository.update(
            TicketStruct.__name__, "ticket_id", str(ref_dto._id), my_audit.asDict()
        )

        return my_audit.asDict()

    def delete(self, write_uid, ticket_id) -> bool:
        self.update(write_uid, ticket_id, dict())

        return True
