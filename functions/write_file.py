import os 

def write_file(working_directory, file_path, content):
    try:
        # Build absolute paths 
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))

        #ensure the file is inside the permitted directory 
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)


        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"