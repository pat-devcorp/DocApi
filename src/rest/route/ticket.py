from flask import Blueprint, request

from ...presentation.controller.ticket import TicketController
from ..ExceptionHandler import exception_handler
from ..status_code import REQUIRED_FIELD, WRITER_NOT_PROVIDED

ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
@exception_handler
def create_ticket():
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)

    lc = TicketController(
        writeUId, ticket.config["MONGO_SERVER"], ticket.config["RABBITMQ_SERVER"]
    )
    item = lc.create(
        params.get("ticketId"),
        params.get("channelId"),
        params.get("requirement"),
        params.get("because"),
    )

    return (200, item)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
@exception_handler
def fetch_tickets(id=None):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return code, message

    lc = TicketController(
        writeUId, ticket.config["MONGO_SERVER"], ticket.config["RABBITMQ_SERVER"]
    )
    data = lc.get_by_id(id) if id is not None else lc.fetch()

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

    lc = TicketController(
        writeUId, ticket.config["MONGO_SERVER"], ticket.config["RABBITMQ_SERVER"]
    )
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

    lc = TicketController(
        writeUId, ticket.config["MONGO_SERVER"], ticket.config["RABBITMQ_SERVER"]
    )
    item = lc.delete(ticketId)

    return (200, item)
