from functions.get_file_content import get_file_content
from config import MAX_CHARS

lorem = get_file_content("calculator", "lorem.txt")
truncation_message = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'

print("lorem length:", len(lorem))
print("lorem truncated correctly:", lorem.endswith(truncation_message))
print("lorem length > MAX_CHARS:", len(lorem) > MAX_CHARS)

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))