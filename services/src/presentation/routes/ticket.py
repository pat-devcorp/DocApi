from flask import Blueprint, jsonify, request

from ...struct.ticket import TicketStruct
from ..controllers.ticket import Ticket as TicketController

Ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@Ticket.get("/", defaults={"id": None})
@Ticket.get("/<id>")
def get(id: str = None):
    my_ticket_controller = TicketController()

    data = (
        my_ticket_controller.getAll()
        if id is None
        else my_ticket_controller.getByID(id)
    )

    return jsonify(data, 200)


@Ticket.post("/")
def create():
    params = request.get_json()
    allowed_keys = ["ticket_id", "description", "write_uid"]
    df = {k: v for k, v in params.items() if k in allowed_keys}

    my_ticket_controller = TicketController()
    data = my_ticket_controller.create(**df)

    return jsonify(data, 200)


@Ticket.put("/<id>")
def update(ticket_id):
    params = request.get_json()
    allowed_keys = TicketStruct._fields + ["write_uid"]
    df = {k: v for k, v in params.items() if k in allowed_keys}

    my_ticket_controller = TicketController()
    data = my_ticket_controller.update(ticket_id, **df)

    return jsonify(data, 200)


@Ticket.delete("/<id>")
def delete(ticket_id):
    my_ticket_controller = TicketController()
    my_ticket_controller.delete(ticket_id)
