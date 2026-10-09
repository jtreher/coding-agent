import json

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file, write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

##
##    for tool_call in message.tool_calls:
##        function_args = json.loads(tool_call.function.arguments or "{}")
##        print(f"Calling function: {tool_call.function.name}({function_args})")
##

def call_function(tool_call, verbose: bool = False) -> dict:
    name : str = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    dir = "./calculator"
    ret = ""

    print(f" - Calling function: {name}({args})")

    match name:
        case "get_files_info":
            ret = (
                get_files_info(dir, args["directory"])
                    if "directory" in args
                    else get_files_info(dir)
            )
        case "get_file_content":
            ret = get_file_content(dir, args["file_path"])
        case "run_python_file":
            ret = (
                run_python_file(dir, args["file_path"], args["args"]) 
                    if "args" in args 
                    else run_python_file(dir, args["file_path"]) 
            )
        case "write_file":
            ret = write_file(dir, args["file_path"], args["content"])
        case _:
            ret = f"Error: Unknown function: {name}"

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": ret,
    }

    