import os

from src.domain.sticker import StickerInterface
from src.infraestructure.barcode import Barcode
from src.infraestructure.config import Config
from src.infraestructure.sticker import getDatos


def test_createBarcode():
    my_config = Config()
    data = StickerInterface.getMock()
    file_name = data.sticker_id
    Barcode.create(file_name)
    file_path = os.path.join(my_config.ASSETS_PATH, file_name)
    print("---EXPECT")
    print(file_path)
    assert os.path.exists(file_path)


# def test_createBarcodes():
#     my_config = Config()
#     for data in getDatos():
#         file_name = data["sticker_id"]
#         Barcode.create(file_name)
#         file_path = os.path.join(my_config.ASSETS_PATH, file_name)
#         assert os.path.exists(file_path)
