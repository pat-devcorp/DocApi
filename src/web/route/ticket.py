from flask import Blueprint, jsonify, request

from .presentation.controller.ticket import TicketController

TICKET_PATH = "/ticket/%s/"
ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
def createTicket():
    print("---POST ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    data = lc.create()

    return jsonify(data, 200)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def fetchTickets(id=None):
    print("---GET ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    if id is not None:
        params["ticketId"] = id
        datos = lc.getById(params)
    else:
        datos = lc.fetch()

    return jsonify(datos, 200)


@ticket.put("/<id>")
def updateTicket(id):
    print("---PUT ATTEMPT")
    params = request.args.to_dict()
    params["ticketId"] = id
    print(params)

    lc = TicketController(params.get("write_uid"))
    data = lc.update(params)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    print("---DEL ATTEMPT")
    params = request.args.to_dict()
    params["ticketId"] = id
    print(params)

    lc = TicketController(params.get("write_uid"))
    data = lc.delete(params)

    return jsonify(data, 200)


@ticket.get("/pending")
def fetchPendingTicket():
    print("---PENDING TICKET ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    datos = lc.fetchPending(params)

    return jsonify(datos, 200)

@ticket.get("/pending")
def fetchPendingTickets():
    print("---PENDING TICKET ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    datos = lc.fetchPending(params)

    return jsonify(datos, 200)

@ticket.get("/pending")
def fetchPendingProjectTickets():
    print("---PENDING PROJECT TICKETS ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    datos = lc.fetchPendingProject(params)

    return jsonify(datos, 200)


# ## Keyword
# @ticket.post("/<id>/keyword")
# def addTicketKeyword(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     keyword = Keyworddto.create(params.get("Keyword"))

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addKeyword(objId, keyword)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/keyword/<keyword_id>")
# def removeTicketKeyword(id, keyword_id):
#     write_uid = request.args.get("write_uid")
#     objId = TicketHandler.getIdentifier(id)
#     keyword_identifier = Keyworddto.getIdentifier(keyword_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeKeyword(objId, keyword_identifier)

#     return jsonify(data, 200)


# ## Meeting
# @ticket.post("/<id>/meeting")
# def addTicketMeeting(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     meeting = Meetingdto.create(params.get("meeting_date"))

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addMeeting(objId, meeting)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/meeting/<meeting_id>")
# def removeTicketMeeting(id, meeting_id):
#     write_uid = request.args.get("write_uid")
#     objId = TicketHandler.getIdentifier(id)
#     meeting_identifier = Meetingdto.getIdentifier(meeting_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeMeeting(objId, meeting_identifier)

#     return jsonify(data, 200)


# ## Milestones
# @ticket.post("/<id>/milestone")
# def addTicketMilestone(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     milestone = Milestonedto.create(params)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addMeeting(objId, milestone)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/milestone/<milestone_id>")
# def removeTicketMilestone(id, milestone_id):
#     write_uid = request.args.get("write_uid")
#     objId = TicketHandler.getIdentifier(id)
#     milestone_identifier = Milestonedto.getIdentifier(milestone_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeMeeting(objId, milestone_identifier)

#     return jsonify(data, 200)


# ## Add Attachment
# @ticket.post("/<id>/attachment")
# def addAttachment(id):
#     write_uid = request.args.get("write_uid")
#     objId = TicketHandler.getIdentifier(id)
#     uploaded_file = request.files["attachment"]

#     path = TICKET_PATH.format(str(id))
#     file_name = uploadFile.create(uploaded_file, path)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addAttachment(objId, file_name)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/attachment/<file_name>")
# def removeAttachment(id, file_name):
#     write_uid = request.args.get("write_uid")
#     objId = TicketHandler.getIdentifier(id)

#     path = TICKET_PATH.format(str(id))
#     fileExists(file_name, path)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeAttachment(objId, file_name)

#     return jsonify(data, 200)


# ## Member
# @ticket.post("/<id>/member")
# def addTicketMember(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.create(params)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addMeeting(objId, member_identifier)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/member/<member_id>")
# def removeTicketMember(id, member_id):
#     write_uid = request.args.get("write_uid")
#     objId = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(member_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeMember(objId, member_identifier)

#     return jsonify(data, 200)


# ## Assignee
# @ticket.post("/<id>/member/set_assignee")
# def setTicketAssignee(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(params.get("member_id"))

#     lc = TicketController(params.get("write_uid"))
#     data = lc.defineAssignee(objId, member_identifier)

#     return jsonify(data, 200)
