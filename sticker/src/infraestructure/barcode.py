import os
import barcode

from .config import Config


class Barcode:
    @staticmethod
    def create(identifier: str) -> str:
        my_config = Config()
        file_path = os.path.join(my_config.ASSETS_PATH, identifier)
        print(file_path)
        
        ean = barcode.get('ean13', identifier)
        print(ean.get_fullcode())

        ean.save(file_path)
