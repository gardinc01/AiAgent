from functions.get_files_info import get_files_info

tests = [
    ("current directory", "."),
    ("'pkg' directory", "pkg"),
    ("'/bin' directory", "/bin"),
    ("'../' directory", "../"),
]

for label, location in tests:
    print(f"Result for {label}:")
    print(get_files_info("calculator", location))

#print("Result for current directory:")
#print(get_files_info("calculator", "."))
#print("Result for current directory:")
#print(get_files_info("calculator", "pkg"))
#print("Result for current directory:")
#print(get_files_info("calculator", "/bin"))
#print("Result for current directory:")
#print(get_files_info("calculator", "../"))