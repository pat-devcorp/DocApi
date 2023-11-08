from src.infraestructure.broker.brokermock import BrokerMock
from src.infraestructure.repositories.repositorymock import RepositoryMock
from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.interface.InterfaceError import InterfaceError
from src.presentation.interface.ticket import Ticket as TicketInterface
from src.presentation.interface.ticket import TicketDTO


def test_fail_interface_identifier():
    try:
        TicketInterface.getIdentifier("XXXXXX")
        assert False
    except InterfaceError:
        assert True


def test_interface_identifier():
    try:
        TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
        assert True
    except InterfaceError:
        assert False


def test_fail_interface_id_required():
    try:
        test_ticket_dto = {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        }
        TicketInterface.fromDict(test_ticket_dto)
        assert False
    except InterfaceError:
        assert True


def test_interface_fromDict():
    try:
        test_ticket_dto = {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            "description": "Test task",
            "category": 0,
            "state": 0,
        }
        TicketInterface.fromDict(test_ticket_dto)
        assert False
    except InterfaceError:
        assert True


def test_interface_create():
    test_ticket_dto = TicketInterface.create(
        ticket_id="3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        description="Test task",
        category=0,
        state=0,
    )
    assert isinstance(test_ticket_dto, TicketDTO)


## Basic task methods
def getControllerMock():
    my_repository = RepositoryMock()
    my_producer = BrokerMock()
    return TicketController(my_repository, my_producer)


# def test_controller_create():
#     lc = getControllerMock("9999")

#     dto = {
#         "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
#         "description": "This is a ticket",
#     }
#     my_ticket_create_dto = TicketInterface.create(dto)
#     response = lc.create(my_ticket_create_dto)
#     assert response


# def test_controller_get():
#     lc = getControllerMock("9999")

#     response_get = lc.fetch()
#     assert isinstance(response_get, list)


# def test_controller_update():
#     lc = getControllerMock("9999")

#     dto = {
#         "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
#         "description": "This is a ticket modified",
#     }
#     my_ticket_update_dto = TicketInterface.fromDict(dto)
#     response = lc.update(my_ticket_update_dto)
#     assert response


# def test_controller_get_by_id():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     response = lc.getByID(i)
#     assert isinstance(response, dict)


# def test_controller_delete():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     response = lc.delete(i)
#     assert response


# def test_task_member():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_member = MemberInterface.create("8888", 0)
#     response = lc.addMember(i, my_member)
#     assert response


# ## Aggregate for task
# def test_task_keyword():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_keyword = KeywordInterface.create("test")
#     response = lc.addKeyword(i, my_keyword)
#     assert response


# def test_task_meeting():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_meeting = meetingInterface.create(
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
#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_milestone = MilestoneInterface.create(milestone)
#     response = lc.addKeyword(i, my_milestone)
#     assert response


# def test_task_attachment():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_attachment = AttachmentInterface.create("/media/test.md")
#     response = lc.addKeyword(i, my_attachment)
#     assert response


# def test_task_assignee():
#     lc = getControllerMock("9999")

#     i = TicketInterface.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c")
#     my_assignee = MemberInterface.setAssignee(
#         "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c", "240"
#     )
#     response = lc.setAssignee(
#         i,
#     )
#     assert response
