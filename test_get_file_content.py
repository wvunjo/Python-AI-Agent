from functions.get_file_content import get_file_content
from config import MAX_CHARS

result = get_file_content("calculator", "lorem.txt")

assert result.endswith(f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]')
assert len(result) > MAX_CHARS

print("lorem.txt truncation OK")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))