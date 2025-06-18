import os

def write_file(working_directory, file_path, content):
    abs_work_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_work_dir, file_path))

    if not abs_file_path.startswith(abs_work_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory' 

    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
                return f"Error: Creating directory {e}"
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except:
        return f"Error: Writing file {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

