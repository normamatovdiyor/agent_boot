import os
from config import MAX_CHARS
def get_file_content(working_directory: str, file_path: str) -> str:
    abs_path  = os.path.abspath(working_directory)
    file_path_ = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_dir = os.path.commonpath([abs_path, file_path_]) == abs_path
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path_):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_path_, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
            
    except  Exception as e:
        return f"Error: {e}"