import os
from google.genai import types


def get_files_info(working_directory, directory="."):

    
    
    working_dir_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'


    try: 
        lines = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            item_size = os.path.getsize(item_path)

            if os.path.isdir(item_path) == True:
                item_isDir = os.path.isdir(item_path)
            else:
                item_isDir = False

            text = (f"- {item}: file_size={item_size}, is_dir={item_isDir}")
            lines.append(text)
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"