import os
import magic
import subprocess
from ..infraestructure.config import Config

def isValidType(file):
    mime = magic.Magic()
    file_type = mime.from_buffer(file.read(1024))
    return 'text' in file_type  # Adjust the condition as per your allowed types


def isSafe(file) -> str:
    try:
        # Use ClamAV to scan the file for viruses
        subprocess.check_output(['clamscan', '--no-summary', file])
        return True
    except subprocess.CalledProcessError:
        return False
    

def uploadFile(uploaded_file, directory):
    my_config = Config()
    if isValidType(uploaded_file.stream) and isSafe(uploaded_file):
        # Process the file here (e.g., save it to a specific folder)
        uploaded_file.save(os.path.join(my_config.MEDIA_PATH, directory, uploaded_file.filename))
        return 'File uploaded and validated successfully.'
    else:
        return 'Invalid file type or contains a virus.'