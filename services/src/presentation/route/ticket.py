from flask import Blueprint, jsonify, request

from ..controller.ticket import Ticket as TicketController
from ..interface.ticket import Ticket as TicketInterface

ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def get(ticket_id: str = None):
    my_ticket_controller = TicketController()

    if ticket_id is not None:
        params = request.get_json()
        params["ticket_id"] = ticket_id
        my_ticked = TicketInterface.createAcessDTO(params)
        datos = my_ticket_controller.getByID(my_ticked)
    else:
        datos = my_ticket_controller.getAll()

    return jsonify(datos, 200)


@ticket.post("/")
def create():
    params = request.get_json()
    my_ticket_dto = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.create(my_ticket_dto)

    return jsonify(data, 200)


@ticket.put("/<id>")
def update(ticket_id):
    params = request.get_json()
    params["ticket_id"] = ticket_id
    my_ticket_dto = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.update(my_ticket_dto)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def delete(ticket_id):
    params = request.get_json()
    params["ticket_id"] = ticket_id
    my_ticked = TicketInterface.createAcessDTO(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.delete(my_ticked)

    return jsonify(data, 200)
