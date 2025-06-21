import os
from google.genai import types

MAX_CHARS = 10000
def get_file_content(working_directory, file_path):
    print(file_path)
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_work_dir, file_path))
        if not abs_file_path.startswith(abs_work_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        if len(file_content_string) == MAX_CHARS + 1:
            file_content_string = file_content_string[:-1]
            file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error was returned: {e}"

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns files contents as a str truncated to {MAX_CHARS} characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to list contents for, relative to the working_directory",
            ),
        },
    ),
)
