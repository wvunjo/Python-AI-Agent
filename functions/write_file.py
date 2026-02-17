import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        common_path = os.path.commonpath([working_dir_abs, target_file])
        parent_directory = os.path.dirname(target_file)


        if common_path != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(parent_directory, exist_ok=True)
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Safely writes text content to a file within a permitted working directory. "
        "Prevents directory traversal outside the working directory, refuses writing "
        "to directories, creates parent directories if needed, and returns a success "
        "or error message."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path (from the permitted working directory) of the file to write. "
                    "Must not be an absolute path or attempt to access files outside the working directory."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The full text content to write to the file. This will overwrite any existing file content."
                ),
            ),
        },
        required=["file_path", "content"],
    ),
)