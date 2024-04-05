import unittest

import pytest

from src.domain.model.document import Document, DocumentDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService

# from src.presentation.controller.document import DocumentController


class TestDocumentController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document_id = DocumentDomain.get_default_identifier()
        cls.document = {
            "body": "test",
        }
        u = UserService.get_default_identifier()
        r = MockRepositoryClient(cls.document)
        b = MockBrokerClient()
        # cls.controller =  DocumentController(u, r, b)

    def test_new_document(self):
        assert hasattr(self.document_id, "value")
        obj = DocumentDomain.new(self.document_id, **self.document)
        assert isinstance(obj, Document)
        assert isinstance(DocumentDomain.as_dict(obj), dict)

    def test_update_document(self):
        dct = dict(self.document)
        dct.update({"document_id": self.document_id.value})
        obj = DocumentDomain.from_dict(dct)
        assert isinstance(obj, Document)


if __name__ == "__main__":
    unittest.main()
