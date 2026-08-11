import os 
import subprocess
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        fn_rs =""
        abs_path = os.path.abspath(working_directory)
        file_path_ = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, file_path_]) == abs_path
        
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_):
                return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path_.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path]

        if args:
            command.extend(args)

        res = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        returncode = res.returncode
        if returncode !=0:
            fn_rs+=f"Process exited with code {returncode}"
        
        stdout = res.stdout
        stderr = res.stderr
        if not stdout and not stderr:
            fn_rs+="No output produced"

        if stdout:
            fn_rs+=f"STDOUT:{stdout}"
        if stderr:
            fn_rs+=f"STDERR:{stderr}"

        args_r = res.args
        return fn_rs
    except Exception as e:
        return f"Error: executing Python file: {e}"
