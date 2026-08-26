import os 

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    result  = ''
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path 
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if valid_target_dir:
            items = os.listdir(target_dir)
            for item in items:
                size = os.path.getsize(f"{target_dir}/{item}")
                is_dir = os.path.isdir(f"{target_dir}/{item}")
                result = result + f"- {item}: file_size={size} bytes, is_dir={is_dir}\n"
                

            return result
    except  Exception as e:
        return f"Error: {e}"
    