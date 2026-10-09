import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": """
            Gets the content a a file from a path relative to the working
            directory. Returns just the first 10,000 characters.
            """,
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path the the file relative to the working directory. The working directory is provided during system invocation.",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    
    try:
        abs_path =  os.path.abspath(working_directory)

        check_path = os.path.normpath(os.path.join(abs_path, file_path))
        # Check to ensure that the common path between the two is the absolute path
        if os.path.commonpath([abs_path, check_path]) != abs_path: 
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
       
        if not os.path.isfile(check_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        print(file_path)

        with open(check_path, "r") as f:
            contents = f.read(10000)

            # After reading the first MAX_CHARS...
            if f.read(1):
                contents += f'[...File "{check_path}" truncated at 10000 characters]'

            return contents

    except Exception as e:
        return f"Error encountered: {e}"

    
