from collections import namedtuple
from enum import Enum
import re

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


TicketStruct = namedtuple('TicketStruct', [
        "ticket_id", 
        "type_ticket", 
        "description", 
        "state", 
        "audit_id"
    ])

class Ticket:
    ticket_id: str
    type_ticket: TypeTicket
    description: str
    state: StateTicket
    audit_id: AuditId

    @staticmethod
    def validate(input_dict: dict) -> dict:
        errors = dict()
        error_description = Ticket.ensureDescription(input_dict.get("description"))
        if len(error_description) > 0:
            errors.update(error_description)
        return errors

    @staticmethod
    def ensureDescription(description: str) ->str:
        if description is None or len(description) == 0:
            return "\nEmpty description"
        
        if checkers.is_string(description, maximum_lengt=200):
            return "\nMax length exceeded, not allowed"
        return ''

    @staticmethod
    def ensureUuidV4(identity: str):
        if identity is None or len(identity) == 0:
            return "\nEmpty description"
        
        uuid_v4_pattern = re.compile(
            r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
        )
        if not bool(uuid_v4_pattern.match(identity)):
            return "\nIs not a valid identity"
        return ''


    @classmethod
    def fromDict(cls, params):
        my_ticket = {k: v for k, v in params.items() if k in TicketStruct._fields}
        
        cls.create(**my_ticket)

    @classmethod
    def create(
        self,
        ticket_id,
        description,
        type_ticket=TypeTicket.UNDEFINED,
        state=StateTicket.UNDIFINED,
        audit_id=None,
    ) -> TicketStruct:
        my_ticket = {
            'ticket_id': ticket_id,
            'description': description,
            'type_ticket': type_ticket,
            'state': state,
            'audit_id': audit_id
        }
        self.validate(my_ticket)
        return TicketStruct(**my_ticket)
