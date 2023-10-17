from enum import Enum

from dictdiffer import diff

from ..domain.ticket import TicketState
from ..utils.AuditHandler import AuditHandler, AuditStruct
from .ApplicationError import ApplicationError
from .ProducerProtocol import ProducerProtocol, ProducerTopic
from .RepositoryProtocol import RepositoryProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class Ticket:
    _name = "ticket"
    _id = "ticket_id"

    def ensureTicketId(self, ref_ticket_dto):
        my_ticket = self.getByID(ref_ticket_dto)
        if my_ticket is None:
            raise ApplicationError(["Ticket does not exist"])
        return my_ticket

    def __init__(
        self, ref_repository: RepositoryProtocol, ref_producer: ProducerProtocol
    ):
        self.my_repository = ref_repository
        self._producer = ref_producer
        self._fields = [
            "ticket_id",
            "description",
            "category",
            "state",
        ] + list(AuditStruct._fields)

    def stateMachine(self, event: TicketEvent, ref_ticket_dto) -> bool:
        print("---STATE MACHINE---")
        print(ref_ticket_dto)
        topic = ProducerTopic.DEFAULT
        message = {k: v for k, v in ref_ticket_dto._asdict().items()}
        is_ok = False

        if event == TicketEvent.CREATED:
            topic = ProducerTopic.TASK_CREATED
            is_ok = self._create(ref_ticket_dto)
        elif event == TicketEvent.UPDATED:
            topic = ProducerTopic.TASK_UPDATED
            is_ok = self._update(ref_ticket_dto)
        elif event == TicketEvent.DELETED:
            topic = ProducerTopic.TASK_DELETED
            is_ok = self._delete(ref_ticket_dto)

        self._producer.sendMessage(topic, message)
        return is_ok

    def get(self, fields: list = None) -> list:
        return self.my_repository.get(self._name, fields or self._fields)

    def getByID(self, ref_ticket_dto, fields: list = None) -> list:
        return self.my_repository.getByID(
            self._name, self._id, ref_ticket_dto.ticket_id, fields or self._fields
        )

    def _create(self, ref_ticket_dto) -> bool:
        print("---CREATE---")
        my_audit = AuditHandler.create(ref_ticket_dto.write_uid)
        my_ticket = my_audit._asdict() | ref_ticket_dto._asdict()

        self.my_repository.create(self._name, my_ticket)

        return True

    def _update(self, ref_ticket_dto) -> bool:
        print("---UPDATE---")
        my_ticket_entity = self.ensureTicketId(ref_ticket_dto)
        current_ticket = ref_ticket_dto._asdict()
        my_ticket = {
            key: value[1]
            for diff_type, key, value in diff(my_ticket_entity, current_ticket)
            if diff_type == "change" and value[1] is not None
        }
        my_audit = AuditHandler.getUpdateFields(ref_ticket_dto.write_uid)
        my_ticket.update(my_audit)

        self.my_repository.update(
            self._name, self._id, ref_ticket_dto.ticket_id, my_ticket
        )

        print(my_ticket)
        return True

    def _delete(self, ref_ticket_dto) -> bool:
        self.ensureTicketId(ref_ticket_dto)

        my_audit = AuditHandler.getUpdateFields(ref_ticket_dto.write_uid)
        my_audit.update({"state": TicketState.DELETED})

        self.my_repository.update(
            self._name, self._id, ref_ticket_dto.ticket_id, my_audit
        )

        return True
