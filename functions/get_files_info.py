import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    abs_work_dir = os.path.abspath(working_directory)
    abs_dir = abs_work_dir  
    if directory:
        abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_dir.startswith(abs_work_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        return_string = ''
        for file in os.listdir(abs_dir):
            filename = os.path.join(abs_dir, file)
            file_size = os.path.getsize(filename)
            is_dir = False
            if os.path.isdir(filename):
                is_dir = True
            file_str = f'{file}: file_size={file_size}, is_dir={is_dir}'
            return_string += file_str + "\n"
        return return_string
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
