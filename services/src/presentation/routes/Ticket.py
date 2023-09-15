from flask import Blueprint, jsonify, request

from ...domain.ticket import Ticket as TicketDomain
from ..controllers.ticket import Ticket as TicketController

Ticket = Blueprint("ticket", __name__, url_prefix="/ticket")
allowed_keys = TicketDomain.__fields__ + ["write_uid"]


@Ticket.get("/", defaults={"id": None})
@Ticket.get("/<id>")
def get_ticket(id: str = None):
    my_controller = TicketController()

    data = my_controller.get_all() if id is None else my_controller.get_by_id(id)

    return jsonify(data, 200)


@Ticket.post("/")
def create_ticket():
    params = request.get_json()
    df = {k: v for k, v in params.items() if k in allowed_keys}

    my_controller = TicketController()
    data = my_controller.create(**df)

    return jsonify(data, 200)


@Ticket.put("/<id>")
def update_ticket(id):
    params = request.get_json()
    df = {k: v for k, v in params.items() if k in allowed_keys}

    my_controller = TicketController()
    data = my_controller(**df)

    return jsonify(data, 200)
