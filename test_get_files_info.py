from functions.get_files_info import get_files_info


print("Result for current directory:")
result = get_files_info("calculator", ".")
intended_result = result.replace("\n", "\n  ")
print(f"  {intended_result}")

print("Result for 'pkg' directory:")
result = get_files_info("calculator", "pkg")
intended_result = result.replace("\n", "\n  ")
print(f"  {intended_result}")

print("Result for '/bin' directory:")
result = get_files_info("calculator", "/bin")
intended_result = result.replace("\n", "\n  ")
print(f"  {intended_result}")

print("Result for '../' directory:")
result = get_files_info("calculator", "../")
intended_result = result.replace("\n", "\n  ")
print(f"  {intended_result}")