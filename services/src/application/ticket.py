from enum import Enum

from ..infraestructure.producer import Producer
from .ApplicationError import ApplicationError
from .repositoryProtocol import RepositoryProtocol


class TicketEvent(Enum):
    CREATED = "C"
    UPDATED = "U"
    DELETED = "D"


class Ticket:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self._fields = TicketStruct._fields + AuditStruct._fields
        self._producer = Producer()

    def stateMachine(self, write_uid, event: TicketEvent, ref_ticket: TicketInterface) -> dict:
        print("---DTO---")
        kafka_topic = ""
        message = ""
        current_ticket = TicketDomain(ref_ticket) 
        new_ticket = None

        if event.CREATED:
            kafka_topic = f"TICKET CREATED: {current_ticket.ticket_id}"
            new_ticket = self._create(write_uid, current_ticket)
        if event.DELETED:
            kafka_topic = f"TICKET DELETED: {current_ticket.ticket_id}"
            new_ticket = self.delete(write_uid, current_ticket.ticket_id)
        if event.UPDATED:
            kafka_topic = f"TICKET UPDATED: {current_ticket.ticket_id}"
            new_ticket = self._update(
                write_uid, current_ticket.ticket_id, current_ticket
            )

        # self._producer.send_message(kafka_topic, message)
        return new_ticket.asDict()

    def ensureTicketId(self, ticket_id: Identity) -> None:
        my_ticket = self.getByID(ticket_id)
        if not my_ticket:
            return None
        return my_ticket

    def getAll(self) -> list:
        return self.my_repository.get(TicketStruct.__name__, self._fields)

    def getByID(self, ticket_id) -> dict:
        return self.my_repository.getByID(
            TicketStruct.__name__, "ticket_id", ticket_id, self._fields
        )

    def _create(self, write_uid, my_struct: TicketDomain) -> TicketDomain:
        my_audit = AuditDomain._create(write_uid)
        my_ticket = {k: v for k, v in my_struct._asdict().items()}
        my_ticket._update(my_audit._asdict())

        self.my_repository._create(TicketStruct.__name__, my_ticket)

        return my_ticket

    def _update(self, write_uid, my_struct: TicketDomain) -> TicketDomain:
        my_ticket = self.ensureTicketId(my_struct.ticket_id)
        if not my_ticket:
            raise ApplicationError(["Ticket does not exist"])

        my_audit = AuditDomain.fromDict(my_ticket)
        my_ticket = {k: v for k, v in my_struct._asdict().items()}
        my_ticket._update(my_audit._asdict())

        self.my_repository._update(
            TicketStruct.__name__, "ticket_id", str(my_struct._id), my_audit._asdict()
        )

        return my_audit

    def delete(self, write_uid, ticket_id: Identity):
        my_ticket = self._update(write_uid, ticket_id, dict())

        return my_ticket
