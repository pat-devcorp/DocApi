from .InterfaceError import InterfaceError
from ...struct.ticket import TicketBaseStruct, TicketStruct

class TicketCreate:
    @classmethod
    def fromDict(params: dict) -> dict:
        required_params = TicketBaseStruct._fields
        my_ticket_dto = {k: v for k, v in params.items() if k in required_params}
        missing_params = set(required_params) - set(my_ticket_dto.keys())
        if missing_params:
            raise InterfaceError(list(missing_params))
        return my_ticket_dto
    
class TicketUpdate:
    @classmethod
    def fromDict(params: dict) -> dict:
        required_params = TicketStruct._fields
        my_ticket_dto = {k: v for k, v in params.items() if k in required_params}
        missing_params = set(required_params) - set(my_ticket_dto.keys())
        if missing_params:
            raise InterfaceError(list(missing_params))
        return my_ticket_dto