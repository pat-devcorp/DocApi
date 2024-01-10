from infrastructure.broker.BrokerMock import BrokerMock
from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.dto.ticket import TicketDto, TicketHandler
from task.src.infrastructure.repositories.RepositoryMock import RepositoryMock


def getTicketId():
    return "87378b40-894c-11ee-b9d1-0242ac120002"


# def test_fail_interface_identifier():
#     try:
#         TicketHandler.getIdentifier("XXXXXX")
#         assert False
#     except Exception:
#         assert True


# def test_interface_identifier():
#     try:
#         TicketHandler.getIdentifier(getTicketId())
#         assert True
#     except Exception:
#         assert False


# def test_interface_fromDict():
#     try:
#         dto = {
#             "description": "Test task",
#             "category": 0,
#             "state": 0,
#         }
#         TicketHandler.fromDict(dto)
#         assert False
#     except Exception:
#         assert True


# def test_interface_create():
#     dto = TicketHandler.create(
#         description="Test task",
#         category=0,
#         state=0,
#     )
#     assert isinstance(dto, TicketDto)


# ## Basic task methods
# def getControllerMock(writeUId):
#     my_repository = RepositoryMock()
#     my_producer = BrokerMock()
#     return TicketController(writeUId, my_repository, my_producer)


# def test_controller_create():
#     lc = getControllerMock("9999")

#     dto = TicketHandler.create(getTicketId(), "This is a ticket")
#     response = lc.create(dto)
#     assert response


# def test_controller_get():
#     lc = getControllerMock("9999")

#     response_get = lc.fetch()
#     assert isinstance(response_get, list)


# def test_controller_update():
#     lc = getControllerMock("9999")

#     identifier = getTicketId()

#     data = {
#         "ticketId": identifier,
#         "description": "This is a ticket modified",
#     }
#     dto = TicketHandler.fromDict(data)
#     identifier = lc.prepareIdentifier(identifier)
#     response = lc.update(identifier, dto)
#     assert response


# def test_controller_get_by_id():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     response = lc.getById(i)
#     assert isinstance(response, dict)


# def test_controller_delete():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     response = lc.delete(i)
#     assert response


# def test_task_member():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_member = Memberdto.create("8888", 0)
#     response = lc.addMember(i, my_member)
#     assert response


# ## Aggregate for task
# def test_task_keyword():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_keyword = Keyworddto.create("test")
#     response = lc.addKeyword(i, my_keyword)
#     assert response


# def test_task_meeting():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_meeting = meetingdto.create(
#         subject="Dealing with bugs",
#         meeting_date="03/10/2023 16:30",
#     )
#     response = lc.addKeyword(i, my_meeting)
#     assert response


# def test_task_cheklist():
#     lc = getControllerMock("9999")

#     milestone = {
#         "name": "Milestone for Project",
#         "items": [
#             "get notifications about project",
#             "generate documentation for project",
#         ],
#     }
#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_milestone = Milestonedto.create(milestone)
#     response = lc.addKeyword(i, my_milestone)
#     assert response


# def test_task_attachment():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_attachment = Attachmentdto.create("/media/test.md")
#     response = lc.addKeyword(i, my_attachment)
#     assert response


# def test_task_assignee():
#     lc = getControllerMock("9999")

#     i = TicketHandler.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_assignee = Memberdto.setAssignee(
#         "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c", "240"
#     )
#     response = lc.setAssignee(
#         i,
#     )
#     assert response
