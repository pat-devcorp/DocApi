import os
from io import BytesIO

import pytest
from PIL import Image as ImageHelper

from src.domain.model.image import Image, ImageDomain
from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.image import ImageController

image_id = ImageDomain.get_default_identifier()
my_config = Bootstrap()
image_path = os.path.join(my_config.IMAGE_PATH, "tmp")
image = {
    "path": image_path,
}


def get_image():
    # Create a mock image for testing
    image = ImageHelper.new("RGB", (100, 100), color="red")
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    image_bytes.filename = "test_image.png"

    return image_bytes


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient(image)
    b = MockBrokerClient()
    return ImageController(u, r, b)


def test_new_image():
    assert hasattr(image_id, "value")
    img = get_image()
    obj = ImageDomain.new(img, image_id, image_path)
    assert isinstance(obj, Image)
    assert isinstance(ImageDomain.as_dict(obj), dict)
    os.rmdir(image_path)


def test_update_image():
    dct = dict(image)
    dct.update({"image_id": image_id.value + ".png"})
    obj = ImageDomain.from_dict(dct)
    assert isinstance(obj, Image)
