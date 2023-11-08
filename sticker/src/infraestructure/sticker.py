import json


def getDatos():
    file_path = "sticker.json"
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            if isinstance(data, list):
                return data
            else:
                raise ValueError("JSON file does not contain an array of objects.")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")
