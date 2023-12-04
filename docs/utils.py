import inspect
import os


def getParamsInfo(class_obj, method_name):
    method = getattr(class_obj, method_name, None)

    if method is not None and inspect.ismethod(method):
        signature = inspect.signature(method)
        params_info = {}

        for param_name, param in signature.parameters.items():
            param_type = (
                str(param.annotation).split("'")[1]
                if param.annotation != param.empty
                else None
            )
            param_default = param.default if param.default != param.empty else None

            params_info[param_name] = {"type": param_type, "default": param_default}

        return params_info
    else:
        return None


def test_getParamsInfo():
    # Example usage
    class MyClass:
        def __init__(self, param1: int = 10, param2: str = "default"):
            pass

    result = getParamsInfo(MyClass, "__init__")
    print(result)


def findTextInFiles(start_string, folder_directory, exclude_types=[]):
    result_text = ""

    for root, dirs, files in os.walk(folder_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension not in exclude_types:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_content = f.read()

                    if file_content.startswith(start_string):
                        result_text += file_content + "\n\n"

    return result_text


def test_findTextInFiles():
    # Example usage
    search_string = "Hello"
    directory_path = "/home/pat/web/TaskApi/src"
    exclude_file_types = [".http", ".log"]  # Add file extensions to exclude

    result = findTextInFiles(search_string, directory_path, exclude_file_types)
    print(result)
