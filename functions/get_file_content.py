import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        common_path = os.path.commonpath([working_dir_abs, target_file])
        if common_path != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):  # Check if there's more content beyond MAX_CHARS
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Safely reads a file within a permitted working directory. "
        "Prevents directory traversal outside the working directory, "
        "validates file existence, and limits the number of characters returned. "
        "Returns error messages for invalid access attempts."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path of the file to read within the permitted "
                    "working directory. Must not be an absolute path or attempt "
                    "to access files outside the working directory."
                ),
            ),
        },
        required=["file_path"],
    ),
)