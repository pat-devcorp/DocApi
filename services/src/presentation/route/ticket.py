from flask import Blueprint, jsonify, request

from ..controller.ticket import Ticket as TicketController
from ..interface.ticket import TicketCreate as TicketCreateInterface
from ..interface.ticket import TicketUpdate as TicketUpdateInterface

ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def get(id: str = None):
    my_ticket_controller = TicketController()

    data = (
        my_ticket_controller.getAll()
        if id is None
        else my_ticket_controller.getByID(id)
    )

    return jsonify(data, 200)


@ticket.post("/")
def create():
    params = request.get_json()
    my_ticket_dto = TicketCreateInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.create(**my_ticket_dto)

    return jsonify(data, 200)


@ticket.put("/<id>")
def update(ticket_id):
    params = request.get_json()

    my_ticket_dto = TicketUpdateInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.update(ticket_id, **my_ticket_dto)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def delete(ticket_id):
    my_ticket_controller = TicketController()
    my_ticket_controller.delete(ticket_id)
