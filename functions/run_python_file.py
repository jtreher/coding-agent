import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to the working directory where the python file is to run, must be a .py file. The working directory is added during function invocation.",
                },
                "args" : {
                    "type": "array",
                    "description" : "arguments to supply to the file being run by python",
                    "items" : {
                        "type":"string",
                    }
                }
            },
            "required" : ["file_path"]
        },
    },
}


def run_python_file(working_directory: str, file_path: str, args: list[str]=[]) -> str:
    try:
        abs_path = os.path.abspath(working_directory)

        check_path = os.path.normpath(os.path.join(abs_path, file_path))

        if os.path.commonpath([abs_path, check_path]) != abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working diretory.'

        if not os.path.isfile(check_path):
            return f'Error: "{file_path}" does not exist or it is not a regular file.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        command = ["python", check_path]

        if len(args) > 0:
            command.extend(args)

        completed_process = subprocess.run(
            command, 
            capture_output=True, 
#            stdout=out, 
 #           stderr=err, 
            text=True, 
            timeout=30,
            cwd=working_directory
        )
            
        return_string = ""

        if completed_process.returncode > 0:
            return_string += f"Process exited with code {completed_process.returncode}\n"


        if len(completed_process.stderr) == 0 and len(completed_process.stdout) == 0:
            return_string += "No output produced.\n"
        elif len(completed_process.stderr) > 0:
            return_string += f"STDERR: {completed_process.stderr}\n"
        elif len(completed_process.stdout) > 0:
            return_string += f"STDOUT: {completed_process.stdout}\n"

        return return_string


    except Exception as e:
        return f"Error encounter: {e}"
