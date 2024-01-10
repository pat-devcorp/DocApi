from flask import Blueprint, jsonify, request

from ...presentation.controller.ticket import TicketController

TICKET_PATH = "/ticket/%s/"
ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
def createTicket():
    params = request.args.to_dict()

    if writeUId := params.get("writeUId"):
        return jsonify(*WRITER_NOT_PROVIDED)

    lc = TicketController(writeUId)
    item = lc.create()

    return jsonify(item, 200)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def fetchTickets(id=None):
    params = request.args.to_dict()

    if writeUId := params.get("writeUId"):
        return jsonify(*WRITER_NOT_PROVIDED)

    lc = TicketController(writeUId)
    if id is not None:
        data = lc.getById(id)
    else:
        data = lc.fetch()

    return jsonify(data, 200)


@ticket.put("/<id>")
def updateTicket(id):
    params = request.args.to_dict()
    
    if writeUId := params.get("writeUId"):
        return jsonify(*WRITER_NOT_PROVIDED)
    if ticketId := params.get("ticketId"):
        return jsonify(*REQUIRED_FIELD)

    lc = TicketController(writeUId)
    params["ticketId"] = ticketId
    item = lc.update(params)

    return jsonify(item, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    params = request.args.to_dict()

    if writeUId := params.get("writeUId"):
        return jsonify(*WRITER_NOT_PROVIDED)
    if ticketId := params.get("ticketId"):
        return jsonify(*REQUIRED_FIELD)

    lc = TicketController(writeUId)
    item = lc.delete(ticketId)

    return jsonify(item, 200)


# @ticket.get("/pending")
# def fetchPendingTicket():
#     params = request.args.to_dict()

#     if writeUId := params.get("writeUId"):
#         return jsonify(*WRITER_NOT_PROVIDED)
#     if ticketId := params.get("ticketId"):
#         return jsonify(*REQUIRED_FIELD)

#     lc = TicketController(writeUId)
#     data = lc.fetchPending(params)

#     return jsonify(data, 200)


# @ticket.get("/pending")
# def fetchPendingTickets():
#     print("---PENDING TICKET ATTEMPT")
#     params = request.args.to_dict()
#     print(params)

#     lc = TicketController(writeUId)
#     data = lc.fetchPending(params)

#     return jsonify(data, 200)


# @ticket.get("/pending")
# def fetchPendingProjectTickets():
#     print("---PENDING PROJECT TICKETS ATTEMPT")
#     params = request.args.to_dict()
#     print(params)

#     lc = TicketController(writeUId)
#     data = lc.fetchPendingProject(params)

#     return jsonify(data, 200)


# ## Keyword
# @ticket.post("/<id>/keyword")
# def addTicketKeyword(id):
#     writeUId = request.args.get("writeUId")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     keyword = Keyworddto.create(params.get("Keyword"))

#     lc = TicketController(writeUId)
#     item = lc.addKeyword(objId, keyword)

#     return jsonify(item, 200)


# @ticket.delete("/<id>/keyword/<keyword_id>")
# def removeTicketKeyword(id, keyword_id):
#     writeUId = request.args.get("writeUId")
#     objId = TicketHandler.getIdentifier(id)
#     keyword_identifier = Keyworddto.getIdentifier(keyword_id)

#     lc = TicketController(writeUId)
#     item = lc.removeKeyword(objId, keyword_identifier)

#     return jsonify(item, 200)


# ## Meeting
# @ticket.post("/<id>/meeting")
# def addTicketMeeting(id):
#     writeUId = request.args.get("writeUId")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     meeting = Meetingdto.create(params.get("meeting_date"))

#     lc = TicketController(writeUId)
#     item = lc.addMeeting(objId, meeting)

#     return jsonify(item, 200)


# @ticket.delete("/<id>/meeting/<meeting_id>")
# def removeTicketMeeting(id, meeting_id):
#     writeUId = request.args.get("writeUId")
#     objId = TicketHandler.getIdentifier(id)
#     meeting_identifier = Meetingdto.getIdentifier(meeting_id)

#     lc = TicketController(writeUId)
#     item = lc.removeMeeting(objId, meeting_identifier)

#     return jsonify(item, 200)


# ## Milestones
# @ticket.post("/<id>/milestone")
# def addTicketMilestone(id):
#     writeUId = request.args.get("writeUId")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     milestone = Milestonedto.create(params)

#     lc = TicketController(writeUId)
#     item = lc.addMeeting(objId, milestone)

#     return jsonify(item, 200)


# @ticket.delete("/<id>/milestone/<milestone_id>")
# def removeTicketMilestone(id, milestone_id):
#     writeUId = request.args.get("writeUId")
#     objId = TicketHandler.getIdentifier(id)
#     milestone_identifier = Milestonedto.getIdentifier(milestone_id)

#     lc = TicketController(writeUId)
#     item = lc.removeMeeting(objId, milestone_identifier)

#     return jsonify(item, 200)


# ## Add Attachment
# @ticket.post("/<id>/attachment")
# def addAttachment(id):
#     writeUId = request.args.get("writeUId")
#     objId = TicketHandler.getIdentifier(id)
#     uploaded_file = request.files["attachment"]

#     path = TICKET_PATH.format(str(id))
#     file_name = uploadFile.create(uploaded_file, path)

#     lc = TicketController(writeUId)
#     item = lc.addAttachment(objId, file_name)

#     return jsonify(item, 200)


# @ticket.delete("/<id>/attachment/<file_name>")
# def removeAttachment(id, file_name):
#     writeUId = request.args.get("writeUId")
#     objId = TicketHandler.getIdentifier(id)

#     path = TICKET_PATH.format(str(id))
#     fileExists(file_name, path)

#     lc = TicketController(writeUId)
#     item = lc.removeAttachment(objId, file_name)

#     return jsonify(item, 200)


# ## Member
# @ticket.post("/<id>/member")
# def addTicketMember(id):
#     writeUId = request.args.get("writeUId")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.create(params)

#     lc = TicketController(writeUId)
#     item = lc.addMeeting(objId, member_identifier)

#     return jsonify(item, 200)


# @ticket.delete("/<id>/member/<member_id>")
# def removeTicketMember(id, member_id):
#     writeUId = request.args.get("writeUId")
#     objId = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(member_id)

#     lc = TicketController(writeUId)
#     item = lc.removeMember(objId, member_identifier)

#     return jsonify(item, 200)


# ## Assignee
# @ticket.post("/<id>/member/set_assignee")
# def setTicketAssignee(id):
#     writeUId = request.args.get("writeUId")
#     params = request.args.to_dict()
#     objId = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(params.get("member_id"))

#     lc = TicketController(writeUId)
#     item = lc.defineAssignee(objId, member_identifier)

#     return jsonify(item, 200)
