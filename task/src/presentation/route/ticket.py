from flask import Blueprint, jsonify, request

from ...utils.FileHandler import uploadFile
from ...utils.AuditHandler import AuditHandler
from ..controller.ticket import Ticket as TicketController
from ..interface.ticket import Ticket as TicketInterface

ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
def createTicket():
    params = request.get_json()
    my_ticket_dto = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.create(my_ticket_dto)

    return jsonify(data, 200)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def fetchTicket(id=None):
    my_ticket_controller = TicketController()

    if id is not None:
        TicketInterface.validateIdentity(id)
        datos = my_ticket_controller.getByID(id)
    else:
        datos = my_ticket_controller.fetch()

    return jsonify(datos, 200)


@ticket.put("/<id>")
def updateTicket(id):
    params = request.get_json()
    params["ticket_id"] = id
    my_ticket_dto = TicketInterface.fromDict(params)

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.update(my_ticket_dto)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.delete(params["write_uid"], id)

    return jsonify(data, 200)


## Keyword 
@ticket.post("/<id>/keyword/<keyword>")
def addTicketKeyword(id, keyword):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.addKeyword(id, keyword)

    return jsonify(data, 200)


@ticket.delete("/<id>/member/<keyword_id>")
def removeTicketKeyword(id, keyword_id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.removeKeyword(id, keyword_id)

    return jsonify(data, 200)

## Meeting
@ticket.post("/<id>/keyword/<meeting_date>")
def addTicketKeyword(id, meeting_date):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.addMeeting(id, meeting_date)

    return jsonify(data, 200)


@ticket.delete("/<id>/member/<meeting_id>")
def removeTicketMeeting(id, meeting_id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.removeMeeting(id, meeting_id)

    return jsonify(data, 200)


## Milestones
@ticket.post("/<id>/milestone")
def addTicketMilestone(id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.addMeeting(id, params)

    return jsonify(data, 200)


@ticket.delete("/<id>/milestone/<milestone_id>")
def removeTicketMilestone(id, milestone_id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.removeMeeting(id, milestone_id)

    return jsonify(data, 200)


## Add Attachment
@ticket.post("/<id>/attachment")
def addAttachment():
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    uploaded_file = request.files["attachment"]
    attachment_path = uploadFile(uploaded_file)
    
    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.addAttachment(id, attachment_path)

    return jsonify(data, 200)


## Member
@ticket.post("/<id>/member/<member_id>")
def addTicketMember(id, member_id):
    TicketInterface.validateIdentity(id)
    AuditHandler.validateIdentity(member_id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.addMeeting(id, member_id)

    return jsonify(data, 200)


@ticket.delete("/<id>/member/<member_id>")
def removeTicketMember(id, member_id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.removeMember(id, member_id)

    return jsonify(data, 200)


## Assignee
@ticket.post("/<id>/member/set_assignee/<member_id>")
def addTicketAssignee(id, member_id):
    TicketInterface.validateIdentity(id)
    params = request.get_json()

    my_ticket_controller = TicketController(params["write_uid"])
    data = my_ticket_controller.addMeeting(id, member_id)

    return jsonify(data, 200)