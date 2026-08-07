from functions.get_files_info import get_files_info

def main():
    first_res = get_files_info("calculator", ".")
    second_res = get_files_info("calculator", "pkg")
    third_res = get_files_info("calculator", "/bin")
    fourth_res = get_files_info("calculator", "../")

    print(f"Result for current directory:\n{first_res}\nResult for 'pkg' directory:\n{second_res}\nResult for '/bin' directory:\n{third_res}\nesult for '../' directory:\n{fourth_res}")

main()