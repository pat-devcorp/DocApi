from typing import Protocol


class DomainProtocol(Protocol):
    def set_identifier(obj_id):
        pass

    def from_dict(task_id, params):
        pass

    def new():
        pass
