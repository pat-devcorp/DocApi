from flask import Blueprint, jsonify, request

from ..controller.ticket import Ticket as TicketController
from ..dto.ticket import TicketHandler

TICKET_PATH = "/ticket/%s/"
ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
def createTicket():
    write_uid = request.args.get("write_uid")
    params = request.get_json()
    my_ticket_dto = TicketHandler.create(
        params.get("ticket_id"),
        params.get("description"),
        params.get("category"),
        params.get("state"),
    )

    lc = TicketController(write_uid)
    data = lc.create(my_ticket_dto)

    return jsonify(data, 200)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def fetchTicket(id=None):
    write_uid = request.args.get("write_uid")
    lc = TicketController(write_uid)

    if id is not None:
        identifier = TicketHandler.getIdentifier(id)
        datos = lc.getByID(identifier)
    else:
        datos = lc.fetch()

    return jsonify(datos, 200)


@ticket.put("/<id>")
def updateTicket(id):
    write_uid = request.args.get("write_uid")
    params = request.get_json()
    params["ticket_id"] = id
    my_ticket_dto = TicketHandler.fromDict(params)

    lc = TicketController(write_uid)
    data = lc.update(my_ticket_dto)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    write_uid = request.args.get("write_uid")
    identifier = TicketHandler.getIdentifier(id)

    lc = TicketController(write_uid)
    data = lc.delete(identifier)

    return jsonify(data, 200)


# ## Keyword
# @ticket.post("/<id>/keyword")
# def addTicketKeyword(id):
#     write_uid = request.args.get("write_uid")
#     params = request.get_json()
#     identifier = TicketHandler.getIdentifier(id)
#     keyword = Keyworddto.create(params.get("Keyword"))

#     lc = TicketController(write_uid)
#     data = lc.addKeyword(identifier, keyword)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/keyword/<keyword_id>")
# def removeTicketKeyword(id, keyword_id):
#     write_uid = request.args.get("write_uid")
#     identifier = TicketHandler.getIdentifier(id)
#     keyword_identifier = Keyworddto.getIdentifier(keyword_id)

#     lc = TicketController(write_uid)
#     data = lc.removeKeyword(identifier, keyword_identifier)

#     return jsonify(data, 200)


# ## Meeting
# @ticket.post("/<id>/meeting")
# def addTicketMeeting(id):
#     write_uid = request.args.get("write_uid")
#     params = request.get_json()
#     identifier = TicketHandler.getIdentifier(id)
#     meeting = Meetingdto.create(params.get("meeting_date"))

#     lc = TicketController(write_uid)
#     data = lc.addMeeting(identifier, meeting)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/meeting/<meeting_id>")
# def removeTicketMeeting(id, meeting_id):
#     write_uid = request.args.get("write_uid")
#     identifier = TicketHandler.getIdentifier(id)
#     meeting_identifier = Meetingdto.getIdentifier(meeting_id)

#     lc = TicketController(write_uid)
#     data = lc.removeMeeting(identifier, meeting_identifier)

#     return jsonify(data, 200)


# ## Milestones
# @ticket.post("/<id>/milestone")
# def addTicketMilestone(id):
#     write_uid = request.args.get("write_uid")
#     params = request.get_json()
#     identifier = TicketHandler.getIdentifier(id)
#     milestone = Milestonedto.create(params)

#     lc = TicketController(write_uid)
#     data = lc.addMeeting(identifier, milestone)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/milestone/<milestone_id>")
# def removeTicketMilestone(id, milestone_id):
#     write_uid = request.args.get("write_uid")
#     identifier = TicketHandler.getIdentifier(id)
#     milestone_identifier = Milestonedto.getIdentifier(milestone_id)

#     lc = TicketController(write_uid)
#     data = lc.removeMeeting(identifier, milestone_identifier)

#     return jsonify(data, 200)


# ## Add Attachment
# @ticket.post("/<id>/attachment")
# def addAttachment(id):
#     write_uid = request.args.get("write_uid")
#     identifier = TicketHandler.getIdentifier(id)
#     uploaded_file = request.files["attachment"]

#     path = TICKET_PATH.format(str(id))
#     file_name = uploadFile.create(uploaded_file, path)

#     lc = TicketController(write_uid)
#     data = lc.addAttachment(identifier, file_name)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/attachment/<file_name>")
# def removeAttachment(id, file_name):
#     write_uid = request.args.get("write_uid")
#     identifier = TicketHandler.getIdentifier(id)

#     path = TICKET_PATH.format(str(id))
#     fileExists(file_name, path)

#     lc = TicketController(write_uid)
#     data = lc.removeAttachment(identifier, file_name)

#     return jsonify(data, 200)


# ## Member
# @ticket.post("/<id>/member")
# def addTicketMember(id):
#     write_uid = request.args.get("write_uid")
#     params = request.get_json()
#     identifier = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.create(params)

#     lc = TicketController(write_uid)
#     data = lc.addMeeting(identifier, member_identifier)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/member/<member_id>")
# def removeTicketMember(id, member_id):
#     write_uid = request.args.get("write_uid")
#     identifier = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(member_id)

#     lc = TicketController(write_uid)
#     data = lc.removeMember(identifier, member_identifier)

#     return jsonify(data, 200)


# ## Assignee
# @ticket.post("/<id>/member/set_assignee")
# def setTicketAssignee(id):
#     write_uid = request.args.get("write_uid")
#     params = request.get_json()
#     identifier = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(params.get("member_id"))

#     lc = TicketController(write_uid)
#     data = lc.defineAssignee(identifier, member_identifier)

#     return jsonify(data, 200)
