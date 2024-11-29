import os
import unittest
from io import BytesIO

import pytest
from PIL import Image as ImageHelper

from src.domain.DomainError import DomainError
from src.domain.identifier_handler import IdentifierHandler
from src.domain.model.image import Image, ImageDomain
from src.domain.model.status_code import FIELD_REQUIRED, INVALID_FORMAT
from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.my_mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.image import ImageController


class TestImageController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_config = Bootstrap()
        cls.image_path = os.path.join(cls.my_config.IMAGE_PATH, "tmp")
        os.makedirs(cls.image_path, exist_ok=True)
        cls.image = ImageDomain.get_valid_image(cls.image_path, ".png")
        cls.image_id = ImageDomain.set_identifier(cls.image.image_id)
        cls.invalid_image = ImageDomain.get_invalid_image()
        u = UserService.get_default_identifier()
        r = MockRepositoryClient(cls.image)
        b = MockBrokerClient()
        cls.controller = ImageController(u, cls.image_path, r, b)
        image = ImageHelper.new("RGB", (100, 100), color="red")
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        image_bytes.filename = "test_image.png"
        cls.img = image_bytes

    # @classmethod
    # def tearDownClass(cls):
    #     # Clean up the temporary directory after testing
    #     for file_name in os.listdir(cls.image_path):
    #         file_path = os.path.join(cls.image_path, file_name)
    #         os.remove(file_path)
    #     os.rmdir(cls.image_path)

    def test_attrs(self):
        assert isinstance(self.image_id, IdentifierHandler)
        assert hasattr(self.image_id, "value")
        assert isinstance(ImageDomain.as_dict(self.image), dict)
        assert not isinstance(self.invalid_image.image_id, IdentifierHandler)

    def test_new_image(self):
        obj = ImageDomain.new(
            self.img,
            self.image_id,
            self.image.path,
            self.image.attrs,
        )
        self.assertIsInstance(obj, Image)

    # def test_update_image(self):
    #     obj = ImageDomain.from_dict(ImageDomain.as_dict(self.image))
    #     assert isinstance(obj, Image)

    # def test_interface_invalid_params(self):
    #     with pytest.raises(DomainError) as error:
    #         self.controller.create(
    #             None,
    #             self.invalid_image.image_id,
    #             self.invalid_image.attrs,
    #         )
    #         assert error.code == FIELD_REQUIRED[0]

    #     with pytest.raises(DomainError) as error:
    #         self.controller.create(
    #             self.img,
    #             self.invalid_image.image_id,
    #             self.invalid_image.attrs,
    #         )
    #         assert error.code == INVALID_FORMAT[0]


if __name__ == "__main__":
    unittest.main()
