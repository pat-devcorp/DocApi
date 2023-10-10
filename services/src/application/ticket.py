from enum import Enum

from ..utils.AuditHandler import AuditHandler, AuditStruct
from .ApplicationError import ApplicationError
from .ProducerProtocol import ProducerProtocol
from .RepositoryProtocol import RepositoryProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class Ticket:
    my_repository = None

    def __init__(
        self, ref_repository: RepositoryProtocol, ref_producer: ProducerProtocol
    ):
        self.my_repository = ref_repository
        self._name = "ticket"
        self._fields = [
            "ticket_id",
            "description",
            "category",
            "state",
        ] + list(AuditStruct._fields)
        self._producer = ref_producer

    def stateMachine(self, write_uid, event: TicketEvent, ref_ticket: dict) -> dict:
        print("---STATE MACHINE---")
        print(ref_ticket)
        topic = ""
        message = ""
        # current_ticket = TicketDomain(ref_ticket)
        new_ticket = None

        if event == TicketEvent.CREATED:
            topic = f"TICKET CREATED: {ref_ticket.ticket_id}"
            new_ticket = self._create(write_uid, ref_ticket)
        elif event == TicketEvent.UPDATED:
            topic = f"TICKET UPDATED: {ref_ticket.ticket_id}"
            new_ticket = self._update(write_uid, ref_ticket)
        elif event == TicketEvent.DELETED:
            topic = f"TICKET DELETED: {ref_ticket.ticket_id}"
            new_ticket = self._delete(write_uid, ref_ticket.ticket_id)
        else:
            raise ApplicationError("Event not found: {0}".format(event))

        self._producer.send_message(topic, message)
        return new_ticket

    def ensureTicketId(self, ticket_id):
        my_ticket = self.getByID(ticket_id)
        if my_ticket is None:
            raise ApplicationError(["Ticket does not exist"])
        return my_ticket

    def getAll(self) -> list:
        return self.my_repository.get(self._name, self._fields)

    def getByID(self, ticket_id) -> dict:
        return self.my_repository.getByID(
            self._name, "ticket_id", ticket_id, self._fields
        )

    def _create(self, write_uid, ref_dto):
        print("---CREATE---")
        my_audit = AuditHandler.create(write_uid)

        my_ticket = {k: v for k, v in ref_dto._asdict().items()}
        my_ticket.update(my_audit._asdict())

        self.my_repository.create(self._name, my_ticket)

        print(my_ticket)
        return my_ticket

    def _update(self, write_uid, ref_dto):
        print("---UPDATE---")
        my_ticket = self.ensureTicketId(ref_dto.ticket_id)

        old_audit = AuditHandler.fromDict(my_ticket)
        my_audit = AuditHandler.update(write_uid, old_audit)

        my_ticket = {k: v for k, v in ref_dto._asdict().items()}
        my_ticket.update(my_audit._asdict())

        self.my_repository.update(self._name, "ticket_id", str(ref_dto._id), my_ticket)

        print(my_ticket)
        return my_audit

    def _delete(self, write_uid, ticket_id):
        my_ticket = self.ensureTicketId(ticket_id)

        old_audit = AuditHandler.fromDict(my_ticket)
        my_audit = AuditHandler.update(write_uid, old_audit)
        my_ticket.update(my_audit._asdict())

        self.my_repository.update(self._name, "ticket_id", ticket_id, my_ticket)

        return my_ticket
