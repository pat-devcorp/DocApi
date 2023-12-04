from flask import Blueprint, jsonify, request

from ..controller.ticket import Ticket as TicketController

TICKET_PATH = "/ticket/%s/"
ticket = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket.post("/")
def createTicket():
    print("---POST ATTEMPT")
    params = request.args.to_dict()
    print(params)
    lc = TicketController(params.get("write_uid"))
    obj_id = lc.prepareIdentifier(params.get("ticket_id"))
    obj = lc.prepareCreate(obj_id, params)

    data = lc.create(obj)
    return jsonify(data, 200)


@ticket.get("/", defaults={"id": None})
@ticket.get("/<id>")
def fetchTicket(id=None):
    print("---GET ATTEMPT")
    params = request.args.to_dict()
    print(params)
    lc = TicketController(params.get("write_uid"))
    if id is not None:
        obj_id = lc.prepareIdentifier(id)
        datos = lc.getByID(obj_id)
    else:
        datos = lc.fetch()

    return jsonify(datos, 200)


@ticket.put("/<id>")
def updateTicket(id):
    print("---PUT ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    params["ticket_id"] = id
    obj = lc.prepareUpdate(params)
    data = lc.update(obj)

    return jsonify(data, 200)


@ticket.delete("/<id>")
def deleteTicket(id):
    print("---DEL ATTEMPT")
    params = request.args.to_dict()
    print(params)

    lc = TicketController(params.get("write_uid"))
    obj_id = lc.prepareIdentifier(id)
    data = lc.delete(obj_id)

    return jsonify(data, 200)


# ## Keyword
# @ticket.post("/<id>/keyword")
# def addTicketKeyword(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     obj_id = TicketHandler.getIdentifier(id)
#     keyword = Keyworddto.create(params.get("Keyword"))

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addKeyword(obj_id, keyword)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/keyword/<keyword_id>")
# def removeTicketKeyword(id, keyword_id):
#     write_uid = request.args.get("write_uid")
#     obj_id = TicketHandler.getIdentifier(id)
#     keyword_identifier = Keyworddto.getIdentifier(keyword_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeKeyword(obj_id, keyword_identifier)

#     return jsonify(data, 200)


# ## Meeting
# @ticket.post("/<id>/meeting")
# def addTicketMeeting(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     obj_id = TicketHandler.getIdentifier(id)
#     meeting = Meetingdto.create(params.get("meeting_date"))

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addMeeting(obj_id, meeting)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/meeting/<meeting_id>")
# def removeTicketMeeting(id, meeting_id):
#     write_uid = request.args.get("write_uid")
#     obj_id = TicketHandler.getIdentifier(id)
#     meeting_identifier = Meetingdto.getIdentifier(meeting_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeMeeting(obj_id, meeting_identifier)

#     return jsonify(data, 200)


# ## Milestones
# @ticket.post("/<id>/milestone")
# def addTicketMilestone(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     obj_id = TicketHandler.getIdentifier(id)
#     milestone = Milestonedto.create(params)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addMeeting(obj_id, milestone)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/milestone/<milestone_id>")
# def removeTicketMilestone(id, milestone_id):
#     write_uid = request.args.get("write_uid")
#     obj_id = TicketHandler.getIdentifier(id)
#     milestone_identifier = Milestonedto.getIdentifier(milestone_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeMeeting(obj_id, milestone_identifier)

#     return jsonify(data, 200)


# ## Add Attachment
# @ticket.post("/<id>/attachment")
# def addAttachment(id):
#     write_uid = request.args.get("write_uid")
#     obj_id = TicketHandler.getIdentifier(id)
#     uploaded_file = request.files["attachment"]

#     path = TICKET_PATH.format(str(id))
#     file_name = uploadFile.create(uploaded_file, path)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addAttachment(obj_id, file_name)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/attachment/<file_name>")
# def removeAttachment(id, file_name):
#     write_uid = request.args.get("write_uid")
#     obj_id = TicketHandler.getIdentifier(id)

#     path = TICKET_PATH.format(str(id))
#     fileExists(file_name, path)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeAttachment(obj_id, file_name)

#     return jsonify(data, 200)


# ## Member
# @ticket.post("/<id>/member")
# def addTicketMember(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     obj_id = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.create(params)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.addMeeting(obj_id, member_identifier)

#     return jsonify(data, 200)


# @ticket.delete("/<id>/member/<member_id>")
# def removeTicketMember(id, member_id):
#     write_uid = request.args.get("write_uid")
#     obj_id = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(member_id)

#     lc = TicketController(params.get("write_uid"))
#     data = lc.removeMember(obj_id, member_identifier)

#     return jsonify(data, 200)


# ## Assignee
# @ticket.post("/<id>/member/set_assignee")
# def setTicketAssignee(id):
#     write_uid = request.args.get("write_uid")
#     params = request.args.to_dict()
#     obj_id = TicketHandler.getIdentifier(id)
#     member_identifier = Memberdto.getIdentifier(params.get("member_id"))

#     lc = TicketController(params.get("write_uid"))
#     data = lc.defineAssignee(obj_id, member_identifier)

#     return jsonify(data, 200)
