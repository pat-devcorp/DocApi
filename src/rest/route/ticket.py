from flask import Blueprint, request

from ...presentation.controller.ticket import TicketController
from ..ExceptionHandler import exception_handler
from ..http_code import REQUIRED_FIELD, WRITER_NOT_PROVIDED

TICKET_PATH = "/ticket/%s/"
ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
@exception_handler
def create_ticket():
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)

    lc = TicketController(writeUId)
    item = lc.create()

    return (200, item)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
@exception_handler
def fetch_tickets(id=None):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return code, message

    lc = TicketController(writeUId)
    if id is not None:
        data = lc.get_by_id(id)
    else:
        data = lc.fetch()

    return (200, data)


@ticket.put("/<id>")
@exception_handler
def update_ticket(id):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (ticketId := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = TicketController(writeUId)
    item = lc.update(ticketId, params)

    return (200, item)


@ticket.delete("/<id>")
@exception_handler
def delete_ticket(id):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (ticketId := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = TicketController(writeUId)
    item = lc.delete(ticketId)

    return (200, item)
