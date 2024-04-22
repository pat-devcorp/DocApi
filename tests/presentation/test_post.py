import unittest

import pytest

from domain.model.post import Post, PostDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService

# from src.presentation.controller.document import PostController


class TestPostController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.post_id = PostDomain.get_default_identifier()
        cls.document = {
            "body": "test",
        }
        u = UserService.get_default_identifier()
        r = MockRepositoryClient(cls.document)
        b = MockBrokerClient()
        # cls.controller =  PostController(u, r, b)

    def test_new_document(self):
        assert hasattr(self.post_id, "value")
        obj = PostDomain.new(self.post_id, **self.document)
        assert isinstance(obj, Post)
        assert isinstance(PostDomain.as_dict(obj), dict)

    def test_update_document(self):
        dct = dict(self.document)
        dct.update({"post_id": self.post_id.value})
        obj = PostDomain.from_dict(dct)
        assert isinstance(obj, Post)


if __name__ == "__main__":
    unittest.main()
