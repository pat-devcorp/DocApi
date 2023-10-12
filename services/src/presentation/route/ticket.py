from flask import Blueprint, jsonify, request

from ..controller.ticket import Ticket as TicketController
from ..interface.ticket import Ticket as TicketInterface

ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def getTicket(id = None):
    my_ticket_controller = TicketController()

    if id is not None:
        params = request.get_json()
        params["ticket_id"] = id
        my_ticked = TicketInterface.fromDict(params)
        datos = my_ticket_controller.getByID(my_ticked)
    else:
        datos = my_ticket_controller.get()

    return jsonify(datos, 200)


@ticket.post("/")
def createTicket():
    params = request.get_json()
    my_ticket_dto = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.create(my_ticket_dto)

    return jsonify(data, 200)


@ticket.put("/<id>")
def updateTicket(id):
    params = request.get_json()
    params["ticket_id"] = id
    my_ticket_dto = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.update(my_ticket_dto)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    params = request.get_json()
    params["ticket_id"] = id
    my_ticked = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController()
    data = my_ticket_controller.delete(my_ticked)

    return jsonify(data, 200)
