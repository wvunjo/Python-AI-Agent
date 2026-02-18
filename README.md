# Python AI Agent

A Python-based AI coding assistant chatbot powered by Google's Gemini API. This agent can interact with files, execute Python code, and perform various file system operations through natural language conversations.

## ⚠️ IMPORTANT WARNING

**DO NOT GIVE THIS PROGRAM TO OTHERS FOR THEM TO USE!**

This project is **for learning purposes only** and does **NOT** have all the security and safety features that a production AI agent would have. It lacks:

- Comprehensive input validation and sanitization
- Rate limiting and abuse prevention
- Advanced security hardening
- Production-grade error handling
- Comprehensive logging and monitoring
- Access control and authentication
- Resource usage limits
- And many other production-ready security features

**Use this project only for educational purposes and experimentation in controlled environments.**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Function Capabilities](#function-capabilities)
- [Security Considerations](#security-considerations)
- [Limitations](#limitations)
- [Example Usage](#example-usage)

## Overview

This Python AI Agent is a command-line chatbot that uses Google's Gemini 2.5 Flash model to understand natural language requests and execute file system operations. The agent can:

- List files and directories
- Read file contents
- Execute Python files with arguments
- Write or create new files

The agent operates within a restricted working directory (`./calculator` by default) to provide basic security boundaries, though this is **not production-grade security**.

## Features

- **Natural Language Interface**: Interact with the agent using plain English
- **Function Calling**: The agent can call predefined functions based on your requests
- **File Operations**: Read, write, and list files within a restricted directory
- **Python Execution**: Run Python scripts with optional command-line arguments
- **Token Tracking**: Monitor API usage with token counts
- **Verbose Mode**: Get detailed output about function calls and API usage

## How It Works

### High-Level Flow

1. **User Input**: You provide a natural language prompt via command-line arguments
2. **API Request**: The program sends your prompt to Google's Gemini API along with available function schemas
3. **AI Decision**: Gemini analyzes your request and decides whether to:
   - Respond directly with text
   - Call one or more functions to fulfill your request
4. **Function Execution**: If functions are called, they execute within the restricted working directory
5. **Response Loop**: Function results are sent back to Gemini, which can then:
   - Provide a final answer
   - Make additional function calls if needed
6. **Output**: The final response is displayed to you

### Conversation Loop

The agent operates in a conversation loop (up to 20 iterations) where:

- Each iteration can result in function calls
- Function results are added to the conversation context
- The AI can make multiple rounds of function calls before responding
- The loop continues until the AI provides a final text response (no more function calls)

## Architecture

### Core Components

```
Python-AI-Agent/
├── main.py                 # Entry point and conversation loop
├── config.py               # Configuration constants
├── prompts.py              # System prompt for the AI agent
├── functions/              # Function implementations
│   ├── call_function.py   # Function dispatcher
│   ├── get_files_info.py  # List files/directories
│   ├── get_file_content.py # Read file contents
│   ├── run_python_file.py  # Execute Python files
│   └── write_file.py       # Write/create files
└── calculator/             # Example working directory
    ├── main.py
    ├── pkg/
    │   ├── calculator.py
    │   └── render.py
    └── README.md
```

### Key Files Explained

#### `main.py`
- Initializes the Gemini API client
- Parses command-line arguments
- Manages the conversation loop
- Handles function call responses
- Tracks API token usage

#### `functions/call_function.py`
- Defines available functions for the AI
- Dispatches function calls to appropriate handlers
- Injects the working directory for security
- Formats function responses for the API

#### `functions/get_files_info.py`
- Lists files and directories
- Provides file sizes and directory status
- Validates directory access within working directory

#### `functions/get_file_content.py`
- Reads file contents safely
- Prevents directory traversal attacks
- Limits content size (10,000 characters by default)
- Handles encoding and file errors

#### `functions/run_python_file.py`
- Executes Python files via subprocess
- Captures stdout and stderr
- Enforces 30-second timeout
- Validates file paths and extensions

#### `functions/write_file.py`
- Creates or overwrites files
- Creates parent directories if needed
- Prevents writing outside working directory
- Validates file paths

#### `config.py`
- Defines `MAX_CHARS` constant (10,000)
- Used to limit file content reading

#### `prompts.py`
- Contains the system prompt that instructs the AI agent
- Defines the agent's role and capabilities
- Explains path handling (relative paths only)

## Installation

### Prerequisites

- Python 3.13 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Steps

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```
   Or manually:
   ```bash
   pip install google-genai==1.12.1 python-dotenv==1.1.0
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Configuration Constants

Edit `config.py` to adjust:
- `MAX_CHARS`: Maximum characters to read from files (default: 10,000)

### Working Directory

The working directory is hardcoded in `functions/call_function.py`:
```python
args["working_directory"] = "./calculator"
```

To change this, modify line 42 in `functions/call_function.py`.

## Usage

### Basic Usage

```bash
python main.py "your prompt here"
```

### Verbose Mode

Get detailed output about function calls and token usage:

```bash
python main.py "your prompt here" --verbose
```

### Example Commands

```bash
# List files in the calculator directory
python main.py "List all files in the current directory"

# Read a file
python main.py "Read the contents of main.py"

# Execute a Python file
python main.py "Run the calculator with the expression '3 + 5 * 2'"

# Write a new file
python main.py "Create a file called test.txt with the content 'Hello World'"

# Complex multi-step request
python main.py "Read the calculator.py file, then create a test file that imports and tests it"
```

## Project Structure

```
Python-AI-Agent/
├── main.py                      # Main entry point
├── config.py                    # Configuration constants
├── prompts.py                   # System prompt
├── pyproject.toml              # Project dependencies
├── README.md                   # This file
├── functions/                  # Function implementations
│   ├── __init__.py            # (if exists)
│   ├── call_function.py       # Function dispatcher
│   ├── get_files_info.py      # List files function
│   ├── get_file_content.py    # Read file function
│   ├── run_python_file.py     # Execute Python function
│   └── write_file.py          # Write file function
└── calculator/                 # Example working directory
    ├── main.py                # Calculator entry point
    ├── pkg/
    │   ├── calculator.py      # Calculator logic
    │   └── render.py         # Output formatting
    ├── lorem.txt             # Example text file
    ├── pkg/morelorem.txt     # Example text file
    └── README.md             # Calculator documentation
```

## Function Capabilities

### 1. `get_files_info`

**Purpose**: List files and directories

**Parameters**:
- `directory` (optional): Relative path to directory (default: current directory)

**Returns**: List of files with sizes and directory flags

**Example AI Request**: "Show me all files in the pkg directory"

### 2. `get_file_content`

**Purpose**: Read file contents

**Parameters**:
- `file_path` (required): Relative path to file

**Returns**: File contents (truncated if > MAX_CHARS)

**Example AI Request**: "Read the calculator.py file"

### 3. `run_python_file`

**Purpose**: Execute Python files

**Parameters**:
- `file_path` (required): Relative path to Python file
- `args` (optional): List of command-line arguments

**Returns**: Execution output (stdout/stderr) and exit code

**Example AI Request**: "Run main.py with the argument '10 + 20'"

### 4. `write_file`

**Purpose**: Create or overwrite files

**Parameters**:
- `file_path` (required): Relative path to file
- `content` (required): Text content to write

**Returns**: Success message with character count

**Example AI Request**: "Create a file called hello.py that prints 'Hello, World!'"

## Security Considerations

### Current Security Measures

1. **Working Directory Restriction**: All file operations are restricted to a single working directory
2. **Path Validation**: Prevents directory traversal attacks using `os.path.commonpath()`
3. **File Type Validation**: Python execution only works on `.py` files
4. **Execution Timeout**: Python files have a 30-second timeout
5. **Content Limits**: File reading is limited to MAX_CHARS characters

### Security Limitations (Why This Is Not Production-Ready)

⚠️ **This project lacks many critical security features:**

1. **No Input Sanitization**: User prompts are not sanitized before sending to API
2. **No Rate Limiting**: API calls are not rate-limited
3. **Hardcoded Working Directory**: Not configurable or user-specific
4. **No Authentication**: Anyone with API key can use the agent
5. **No Access Control**: No user permissions or role-based access
6. **Limited Error Handling**: Errors may expose sensitive information
7. **No Logging**: No audit trail of operations
8. **No Resource Limits**: No memory or CPU usage limits
9. **Subprocess Security**: Python execution uses basic subprocess without sandboxing
10. **No Validation of File Contents**: Written files are not validated
11. **API Key Exposure Risk**: API key stored in plain text `.env` file

**Do not use this in production or share it with others without understanding these limitations.**

## Limitations

1. **Conversation Limit**: Maximum 20 iterations per conversation
2. **File Size Limit**: Files larger than MAX_CHARS are truncated
3. **Python Only**: Can only execute Python files
4. **Single Working Directory**: All operations restricted to one directory
5. **No State Persistence**: Conversations don't persist between runs
6. **No Multi-User Support**: Single-user only
7. **No Streaming**: Responses are not streamed (wait for complete response)
8. **API Dependency**: Requires internet connection and valid API key
9. **Cost**: Uses paid Gemini API (costs depend on usage)

## Example Usage

### Example 1: Simple File Listing

```bash
python main.py "What files are in the calculator directory?"
```

**Expected Flow**:
1. AI calls `get_files_info` with directory="."
2. Function returns list of files
3. AI formats and displays the response

### Example 2: Reading and Understanding Code

```bash
python main.py "Read calculator.py and explain what it does"
```

**Expected Flow**:
1. AI calls `get_file_content` with file_path="pkg/calculator.py"
2. Function returns file contents
3. AI analyzes the code and provides explanation

### Example 3: Executing Code

```bash
python main.py "Run the calculator with the expression '5 * 3 + 2'"
```

**Expected Flow**:
1. AI calls `run_python_file` with file_path="main.py" and args=["5 * 3 + 2"]
2. Function executes the Python file
3. Function returns stdout/stderr
4. AI displays the result

### Example 4: Creating Files

```bash
python main.py "Create a Python file called test.py that prints 'Hello from AI Agent'"
```

**Expected Flow**:
1. AI calls `write_file` with file_path="test.py" and content="print('Hello from AI Agent')"
2. Function creates the file
3. AI confirms the file was created

### Example 5: Complex Multi-Step Task

```bash
python main.py "Read the calculator code, then create a test file that imports Calculator and tests it with '10 + 5'"
```

**Expected Flow**:
1. AI calls `get_file_content` to read calculator.py
2. AI calls `write_file` to create test file with import and test code
3. AI may call `run_python_file` to execute the test
4. AI provides final summary

## Development Notes

### Testing

Test files are included in the root directory:
- `test_write_file.py`
- `test_run_python_file.py`
- `test_get_files_info.py`
- `test_get_file_content.py`

These can be used to test individual functions independently.

### Extending Functionality

To add new functions:

1. Create a new function file in `functions/`
2. Implement the function with `working_directory` parameter
3. Create a schema using `types.FunctionDeclaration`
4. Add the schema to `available_functions` in `call_function.py`
5. Add the function to the `function_map` in `call_function.py`

### API Model

Currently uses `gemini-2.5-flash`. To change:
- Edit `main.py` line 30: `model = "gemini-2.5-flash"`

## License

This project is for educational purposes only. See the warning at the top of this README.

## Contributing

This is a learning project. Feel free to fork and experiment, but remember: **do not distribute this as a production-ready tool.**

---

**Remember**: This is a learning project. Use responsibly and do not share with others expecting production-grade security or features.
