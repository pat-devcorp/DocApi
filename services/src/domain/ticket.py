from enum import Enum
from uuid import uuid4

from validator_collection import checkers

from .audit import AuditId


class TypeTicket(Enum):
    UNDEFINED = 0
    HOTFIX = 1
    BUGFIX = 2
    FEATURE = 3
    REFACTOR = 4
    DOCS = 5


class StateTicket(Enum):
    UNDIFINED = "U"
    CREATED = "C"
    IN_PROCESS = "P"
    OBSERVE = "O"
    END = "E"


class EventTicket(Enum):
    CREATED = "C"
    IN_PROCESS = "P"
    OBSERVE = "O"
    END = "E"


class TicketId:
    def __init__(self, value=None):
        self._id = value

    def __str__(self):
        return self._id

    @classmethod
    def get_new_id(cls):
        return cls(str(uuid4()))


class Ticket:
    _id: TicketId
    type_ticket: TypeTicket
    description: str
    state: StateTicket
    audit_id: AuditId

    __tablename__ = "ticket"
    __fields__ = ["_id", "type_ticket", "description", "state", "audit_id"]

    @staticmethod
    def validate_schema(input_dict: dict):
        errors = dict()
        error_description = Ticket.ensure_description(input_dict.get("description"))
        if error_description is not None:
            errors.update(error_description)
        return errors

    @staticmethod
    def ensure_description(description):
        if description is not None:
            if checkers.is_string(description, maximum_lengt=200):
                return {"description": "Not allowed"}
        return None

    @classmethod
    def from_dict(cls, params):
        df = {k: v for k, v in params.items() if k in cls.__fields__}

        identity = df.get("_id")
        if identity is not None:
            df._id = TicketId(df._id)
        type_ticket = df.get("type_ticket")

        if type_ticket is not None:
            df.type_ticket = TypeTicket(type_ticket)
        state = df.get("state")

        if state is not None:
            df.state = StateTicket(state)

        return cls(**df)

    def as_dict(self):
        return {
            "_id": str(self._id),
            "type_ticket": self.type_ticket.value,
            "description": self.description,
            "state": self.state.value,
            "audit_id": self.audit_id,
        }

    def __init__(
        self,
        description,
        type_ticket=TypeTicket.UNDEFINED,
        state=StateTicket.UNDIFINED,
        _id=None,
        audit_id=None,
    ):
        self.description = description
        self.type_ticket = type_ticket
        self.state = state
        self._id = _id
        self.audit_id = audit_id

    def create(self):
        self.state_machine(StateTicket.CREATED, EventTicket.CREATED)

    def state_machine(self, state: StateTicket, event: EventTicket):
        if state.CREATED:
            if event.CREATED:
                self.state = StateTicket.CREATED
                self._id = TicketId.get_new_id()
