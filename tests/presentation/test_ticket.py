import unittest

import pytest

from src.domain.DomainError import DomainError
from src.domain.model.ticket import Ticket, TicketDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.ticket import TicketController
from src.domain.model.status_code import FIELD_REQUIRED, ID_NOT_VALID, INVALID_FORMAT


class TestTicketController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ticket = TicketDomain.get_valid_ticket()
        cls.ticket_id = TicketDomain.set_identifier(cls.ticket.ticket_id)
        cls.invalid_ticket = TicketDomain.get_invalid_ticket()
        u = UserService.get_default_identifier()
        r = MockRepositoryClient(TicketDomain.as_dict(cls.ticket))
        b = MockBrokerClient()
        cls.controller = TicketController(u, r, b)

    def test_attrs(self):
        assert hasattr(self.ticket_id, "value")
        assert isinstance(TicketDomain.as_dict(self.ticket), dict)

    def test_new_ticket(self):
        obj = TicketDomain.new(
            self.ticket_id,
            self.ticket.channel_type,
            self.ticket.requirement,
            self.ticket.because,
            self.ticket.state,
        )
        assert isinstance(obj, Ticket)

    def test_new_ticket_adding_attrs(self):
        obj = TicketDomain.new(
            self.ticket_id,
            self.ticket.channel_type,
            self.ticket.requirement,
            self.ticket.because,
            self.ticket.state,
            self.ticket.attrs,
        )
        assert isinstance(obj, Ticket)

    def test_update_ticket(self):
        obj = TicketDomain.from_dict(TicketDomain.as_dict(self.ticket))
        assert isinstance(obj, Ticket)

    def test_interface_invalid_params(self):
        with pytest.raises(DomainError) as error:
            self.controller.create(
                None,
                self.invalid_ticket.channel_type,
                self.invalid_ticket.requirement,
                self.invalid_ticket.because,
                self.invalid_ticket.state,
                self.invalid_ticket.attrs,
            )
            assert error.code == FIELD_REQUIRED[0]

        with pytest.raises(DomainError) as error:
            self.controller.create(
                self.invalid_ticket.ticket_id,
                self.invalid_ticket.channel_type,
                self.invalid_ticket.requirement,
                self.invalid_ticket.because,
                self.invalid_ticket.state,
                self.invalid_ticket.attrs,
            )
            assert error.code == INVALID_FORMAT[0]


if __name__ == "__main__":
    unittest.main()
