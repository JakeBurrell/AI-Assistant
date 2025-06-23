from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_files_content 
from functions.run_python_file import run_python_file, schema_run_python_file 
from functions.write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    functions = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'run_python_file': run_python_file,
        'write_file': write_file
    }
    function_name = function_call_part.name
    function_args = function_call_part.args
    if function_name in functions:
        function_result = functions[function_name](**function_args, working_directory="./calculator")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


