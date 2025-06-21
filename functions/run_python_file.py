import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    abs_work_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_work_dir, file_path))

    if not abs_file_path.startswith(abs_work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not os.path.splitext(abs_file_path)[1] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        process_return = subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True, cwd=abs_work_dir, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not process_return.stderr and not process_return.stdout:
        return "No output produced."
    return_string = f"STDOUT: {process_return.stdout}\nSTDERR: {process_return.stderr}"
    if process_return.returncode != 0:
        return_string += f"\nProcess exited with code {process_return.returncode}"
    return return_string

schema_run_python_file= types.FunctionDeclaration(
    name="run_python_file",
    description=f"Runs a python file specified by the file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Returns the STDOUT and the STDERR from function specified if completed successfully, relative to the working directory.",
            ),
        },
    ),
)
