from flask import Blueprint, request

from ...presentation.controller.ticket import TicketController
from ..ExceptionHandler import exception_handler
from ..status_code import REQUIRED_FIELD, WRITER_NOT_PROVIDED

ticket_route = Blueprint("ticket_route", __name__, url_prefix="/ticket")


@ticket_route.post("/")
@exception_handler
def create_ticket():
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)

    lc = TicketController(
        write_uid,
        ticket_route.config["REPOSITORY_MONGO"],
        ticket_route.config["BROKER_RABBITMQ"],
    )
    item = lc.create(
        params.get("ticket_id"),
        params.get("channel_id"),
        params.get("requirement"),
        params.get("because"),
    )

    return (200, item)


@ticket_route.get("/", defaults={"id": None})
@ticket_route.get("/<id>")
@exception_handler
def fetch_tickets(id=None):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return code, message

    lc = TicketController(
        write_uid,
        ticket_route.config["MONGO_SERVER"],
        ticket_route.config["RABBITMQ_SERVER"],
    )
    data = lc.get_by_id(id) if id is not None else lc.fetch()

    return (200, data)


@ticket_route.put("/<id>")
@exception_handler
def update_ticket(id):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (ticket_id := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = TicketController(
        write_uid,
        ticket_route.config["MONGO_SERVER"],
        ticket_route.config["RABBITMQ_SERVER"],
    )
    item = lc.update(ticket_id, params)

    return (200, item)


@ticket_route.delete("/<id>")
@exception_handler
def delete_ticket(id):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (ticket_id := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = TicketController(
        write_uid,
        ticket_route.config["MONGO_SERVER"],
        ticket_route.config["RABBITMQ_SERVER"],
    )
    item = lc.delete(ticket_id)

    return (200, item)
