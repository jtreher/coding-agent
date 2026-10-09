import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or overwrite contents to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to the working directory where to write the file. The working directory is supplied during invocation by the system.",
                },
                "content" : {
                    "type": "string",
                    "description" : "Content to write to the file",
                }
            },
            "required" : ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    
    try:
        abs_path = os.path.abspath(working_directory)

        check_path = os.path.normpath(os.path.join(abs_path, file_path))

        if os.path.commonpath([abs_path, check_path]) != abs_path:
            return f'Error: Cannot write to "{file_path}". It is outside of working diretory.'

        if os.path.isdir(check_path):
            return f'Error: Cannot write tp "{check_path}. It is a directory.'

        dir_name = os.path.dirname(check_path)

        os.makedirs(dir_name, exist_ok=True)

        with open(file=check_path, mode="w") as f:
            _ = f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e: 
        return f"Error encountered: {e}"

    

    


