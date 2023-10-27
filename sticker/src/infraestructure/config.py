import os


class Config:
    def __init__(self) -> None:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, ".."))
        print("---Path")
        print(self.PROJECT_PATH)

        self.ASSETS_PATH = os.path.join(self.PROJECT_PATH, "assets")
        self.BARCODE_WIDTH = 2.0
        self.BARCODE_HEIGTH = 15.0

        self.DOCS_PATH = os.path.join(self.PROJECT_PATH, "docs")