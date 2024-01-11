from flask import Blueprint, jsonify, request

from ...presentation.controller.ticket import TicketController
from ..HttpHandler import REQUIRED_FIELD, WRITER_NOT_PROVIDED

TICKET_PATH = "/ticket/%s/"
ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
def createTicket():
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return jsonify(code, message)

    lc = TicketController(writeUId)
    item = lc.create()

    return jsonify(item, 200)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def fetchTickets(id=None):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return jsonify(code, message)

    lc = TicketController(writeUId)
    if id is not None:
        data = lc.getById(id)
    else:
        data = lc.fetch()

    return jsonify(data, 200)


@ticket.put("/<id>")
def updateTicket(id):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return jsonify(code, message)
    if (ticketId := params.get("ticketId")) is None:
        code, message = REQUIRED_FIELD
        return jsonify(code, message)

    lc = TicketController(writeUId)
    item = lc.update(ticketId, params)

    return jsonify(item, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return jsonify(code, message)
    if (ticketId := params.get("ticketId")) is None:
        code, message = REQUIRED_FIELD
        return jsonify(code, message)

    lc = TicketController(writeUId)
    item = lc.delete(ticketId)

    return jsonify(item, 200)
