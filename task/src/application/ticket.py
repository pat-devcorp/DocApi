from enum import Enum

from dictdiffer import diff

from ..domain.ticket import TicketState
from ..utils.AuditHandler import AuditHandler, AuditStruct
from .ApplicationError import ApplicationError
from .BrokerTopic import BrokerTopic
from .BrokerProtocol import BrokerProtocol
from .RepositoryProtocol import RepositoryProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class Ticket:
    _name = "ticket"
    _id = "ticket_id"
    _fields = [
            "ticket_id",
            "description",
            "category",
            "state",
    ]

    def __init__(
        self, ref_repository: RepositoryProtocol, ref_broker: BrokerProtocol
    ):
        self.my_repository = ref_repository
        self.my_broker = ref_broker
        self._fields += list(AuditStruct._fields)

    def stateMachine(self, event: TicketEvent, ref_ticket_dto) -> bool:
        print("---STATE MACHINE---")
        print(ref_ticket_dto)
        topic = None
        is_ok = False
        message = {k: v for k, v in ref_ticket_dto._asdict().items()}

        if event == TicketEvent.CREATED:
            topic = BrokerTopic.TASK_CREATED
            is_ok = self._create(ref_ticket_dto)
        elif event == TicketEvent.UPDATED:
            topic = BrokerTopic.TASK_UPDATED
            is_ok = self._update(ref_ticket_dto)
        elif event == TicketEvent.DELETED:
            topic = BrokerTopic.TASK_DELETED
            is_ok = self._delete(ref_ticket_dto)
    
        if topic is not None:
            self.my_broker.sendMessage(topic, message)
        
        return is_ok

    def fetch(self, fields: list = None) -> list:
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
        my_ticket_entity = self.getByID(ref_ticket_dto)
        if my_ticket_entity is None:
            raise ApplicationError(["Ticket does not exist"])
        
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
        if self.getByID(ref_ticket_dto) is None:
            raise ApplicationError(["Ticket does not exist"])

        my_audit = AuditHandler.getUpdateFields(ref_ticket_dto.write_uid)
        my_audit.update({"state": TicketState.DELETED})

        self.my_repository.update(
            self._name, self._id, ref_ticket_dto.ticket_id, my_audit
        )

        return True
