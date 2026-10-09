import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """Working directory is the directory to limit LLM access"""
    try:

        abs_path =  os.path.abspath(working_directory)

        check_path = os.path.normpath(os.path.join(abs_path, directory))

        # Check to ensure that the common path between the two is the absolute path
        if os.path.commonpath([abs_path, check_path]) != abs_path: 
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(check_path):
            return f'Error: "{directory}" is not a directory'
        
        result = ""

        for item in os.listdir(check_path):
            dict_item = {
                "name" : item, 
                "size" : os.path.getsize(os.path.join(check_path, item)),
                "is_dir" : os.path.isdir(os.path.join(check_path, item))
            }
            

            result = result + f'- {dict_item["name"]}: file_size={dict_item["size"]} bytes, is_dir={dict_item["is_dir"]}\n'
                        

        return result
    except Exception as e:
        return f'Error encountered: {e}'


                              

    
