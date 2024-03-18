from typing import Protocol


class DomainProtocol(Protocol):
    def set_identifier(obj_id):
        pass

    def from_dict(ticketId, params):
        pass

    def new():
        pass
