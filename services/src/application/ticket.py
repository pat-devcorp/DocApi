from enum import Enum

from ..infraestructure.producer import Producer
from ..struct.audit import Audit as AuditDomain
from ..struct.audit import AuditStruct
from ..struct.ticket import Ticket as TicketDomain
from ..struct.ticket import TicketState, TicketStruct
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

    def stateMachine(self, write_uid, event: TicketEvent, dto_ref: dict) -> dict:
        print("---DTO---")
        print(dto_ref)
        current_ticket = TicketDomain.fromDict(dto_ref)
        kafka_topic = ""
        message = ""
        new_ticket = None

        if event.CREATED:
            self.state = TicketState.CREATED
            kafka_topic = f"TICKET CREATED: {current_ticket.ticket_id}"
            new_ticket = self.create(write_uid, current_ticket)
        if event.DELETED:
            kafka_topic = f"TICKET DELETED: {current_ticket.ticket_id}"
            new_ticket = self.delete(write_uid, current_ticket.ticket_id)
        if event.UPDATED:
            kafka_topic = f"TICKET UPDATED: {current_ticket.ticket_id}"
            new_ticket = self.update(
                write_uid, current_ticket.ticket_id, current_ticket
            )

        # self._producer.send_message(kafka_topic, message)
        return new_ticket._asdict()

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

    def create(self, write_uid, my_struct: TicketStruct) -> TicketStruct:
        my_audit = AuditDomain.create(write_uid)
        my_ticket = {k: v for k, v in my_struct.__asdict().items()}
        my_ticket.update(my_audit._asdict())

        self.my_repository.create(TicketStruct.__name__, my_ticket._asdict())

        return my_ticket

    def update(self, write_uid, ticket_id, my_struct: TicketStruct) -> TicketStruct:
        my_ticket = self.ensureTicketId(ticket_id)
        if not my_ticket:
            raise ApplicationError(["Ticket does not exist"])

        my_dto_audit = {k: v for k, v in my_ticket if k in AuditStruct._fields}
        my_audit = AuditDomain.update(write_uid, **my_dto_audit)

        self.my_repository.update(
            TicketStruct.__name__, "ticket_id", str(my_struct._id), my_audit._asdict()
        )

        return my_audit

    def delete(self, write_uid, ticket_id) -> TicketStruct:
        my_ticket = self.update(write_uid, ticket_id, dict())

        return my_ticket
