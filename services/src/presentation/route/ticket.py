from flask import Blueprint, jsonify, request

from ..controller.ticket import Ticket as TicketController
from ..interface.ticket import Ticket as TicketHandler

ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def get(ticket_id: str = None):
    my_ticket_controller = TicketController()

    if ticket_id is not None:
        my_ticked_id = TicketHandler.validateIdentity(ticket_id)
        datos = my_ticket_controller.getByID(my_ticked_id)
    else:
        datos = my_ticket_controller.getAll()

    return jsonify(datos, 200)


@ticket.post("/")
def create():
    params = request.get_json()
    my_ticket_dto = TicketHandler.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.create(**my_ticket_dto)

    return jsonify(data, 200)


@ticket.put("/<id>")
def update(ticket_id):
    params = request.get_json()
    my_ticket_dto = TicketHandler.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.update(ticket_id, my_ticket_dto)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def delete(ticket_id):
    my_ticked_id = TicketHandler.validateIdentity(ticket_id)

    my_ticket_controller = TicketController()
    my_ticket_controller.delete(my_ticked_id)
