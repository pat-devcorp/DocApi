import os
import unittest
from io import BytesIO

from src.utils.file_handler import upload_file


class TestUploadFile(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory for testing
        self.media_path = "temp_media"
        os.makedirs(self.media_path, exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory after testing
        for file_name in os.listdir(self.media_path):
            file_path = os.path.join(self.media_path, file_name)
            os.remove(file_path)
        os.rmdir(self.media_path)

    def test_upload_file(self):
        # Create a mock file for testing
        file_data = b"Test file content"
        file_name = "test_file.txt"
        uploaded_file = BytesIO(file_data)
        uploaded_file.filename = file_name

        # Call the function to upload the file
        uploaded_file_path = upload_file(self.media_path, uploaded_file)

        # Assert that the file was successfully uploaded
        self.assertTrue(os.path.exists(uploaded_file_path))
        with open(uploaded_file_path, "rb") as f:
            self.assertEqual(f.read(), file_data)


if __name__ == "__main__":
    unittest.main()
