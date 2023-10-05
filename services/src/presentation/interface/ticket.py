from .InterfaceError import InterfaceError


def newTicket(params: dict) -> dict:
    if params.get("write_uid") is None:
        raise InterfaceError(["User identity is required"])
    
    required_params = ["write_uid", "ticket_id", "description"]
    my_ticket_dto = {k: v for k, v in params.items() if k in required_params}
    missing_params = set(required_params) - set(my_ticket_dto.keys())
    if missing_params:
        raise InterfaceError(list(missing_params))
    return my_ticket_dto


def setTicket(params: dict) -> dict:
    if params.get("write_uid") is None:
        raise InterfaceError(["User identity is required"])
    if params.get("ticket_id") is None:
        raise InterfaceError(["Identifier must be provided"])
    
    required_params = ["write_uid", "ticket_id", "description", "category", "state"]
    my_ticket_dto = {k: v for k, v in params.items() if k in required_params}
    return my_ticket_dto
