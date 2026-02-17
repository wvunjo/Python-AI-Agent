import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        common_path = os.path.commonpath([working_dir_abs, target_file])
        absolute_file_path = os.path.join(working_dir_abs, file_path)
        if common_path != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(command,
                                cwd=working_dir_abs,
                                timeout=30,
                                capture_output=True,
                                text=True)
        output_lines = []
        if not result.returncode == 0:
            output_lines.append(f"Process exited with code {result.returncode}")
        if not (result.stdout or result.stderr):
            output_lines.append("No output produced")
        if result.stdout:
            output_lines.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_lines.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output_lines)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file within the permitted working directory. "
        "Prevents directory traversal outside the working directory, "
        "ensures the file exists and is a .py file, and captures STDOUT "
        "and STDERR output. Returns execution results or error messages."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path (from the permitted working directory) "
                    "of the Python (.py) file to execute. Must not be an "
                    "absolute path or attempt to access files outside the working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of command-line arguments to pass to the Python file. "
                    "Each item should be a separate argument string."
                ),
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        },
        required=["file_path"],  # args is optional
    ),
)