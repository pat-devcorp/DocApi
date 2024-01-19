# from src.domain.DomainError import DomainError
# from src.infrastructure.broker.BrokerMock import BrokerMock
# from src.infrastructure.repositories.RepositoryMock import RepositoryMock
# from src.presentation.controller.ticket import Ticket as TicketController
# from src.presentation.controller.ticket import TicketController


# def getUser():
#     return "9999"


# def test_TaskController():
#     """mermaid
#     classDiagram
#     JSON --> TicketDto :toDict
#     TicketDto --> TicketController
#     class TicketDto{
#         str, description, Test task,
#         TicketCategory, category, TicketCategory.UNDEFINED,
#         TicketTypeCommit, typeCommit, TicketTypeCommit.UNDEFINED,
#         TicketState, state, TicketState.CREATED,
#     }
#     """

#     dto = TicketDto.getMock()
#     my_repository = RepositoryMock(dto.asDict())
#     my_producer = BrokerMock()
#     lc = TicketController(getUser(), my_repository, my_producer)
#     assert lc.doCreate(dto)


# def test_TaskUseCase():
#     current_user = getUser()
#     dto = TicketDto.getMock()
#     r = TicketRepository()
#     lc = TicketController(current_user, r)
#     try:
#         lc.dogetById(dto.ticketId)
#     except DomainError as eu:
#         assert True
#     lc.doCreate(dto)
#     data = lc.dogetById(dto.ticketId)
#     print(f"DATA: {data}")
#     assert data
#     dto.description = "I was updated successfully"
#     lc.doUpdate(dto)
#     datos = lc.fetch()
#     print(f"DATOS: {datos}")
#     assert datos
#     lc.doDelete(dto.ticketId)
