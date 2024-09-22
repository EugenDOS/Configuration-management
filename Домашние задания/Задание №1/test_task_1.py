import sys, task_1
from task_1 import *
from zipfile import ZipFile

# Независимые тестовые данные
zip_path = "test.zip"
user_name = "test_user"
pc_name = "test_pc"

# Тестирование parse_arguments
def test_parse_arguments():
    try:
        sys.argv = ["task_1.py", "test_user", "test_pc", "test.zip"]
        task_1.args = task_1.parse_arguments()
        assert task_1.args.user_name == "test_user"
        assert task_1.args.pc_name == "test_pc"
        assert task_1.args.zip_path == "test.zip"
        print("OK === parse_arguments(), standard mode")
    except Exception as e:
        print(f"ERROR === parse_arguments(), standard mode\n{e}\n")

# Тестирование chmod
def test_chmod():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("test_file.txt", "Test content")
        chmod("755", "test_file.txt")
        assert permissions["test_file.txt"] == 0o755
        print("OK === chmod(), standard mode")
    except Exception as e:
        print(f"ERROR === chmod(), standard mode\n{e}\n")

def test_chmod_invalid_mode():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("test_file.txt", "Test content")
        result = chmod("invalid", "test_file.txt")
        assert "Invalid mode" in result
        print("OK === chmod(), invalid mode")
    except Exception as e:
        print(f"ERROR === chmod(), invalid mode\n{e}\n")

# Тестирование cal
def test_cal_current_month():
    try:
        result = cal()
        current_month = datetime.now().strftime("%B")
        assert current_month in result
        print("OK === cal(), current_month mode")
    except Exception as e:
        print(f"ERROR === cal(), current_month mode\n{e}\n")

def test_cal_specific_month():
    try:
        result = cal(1, 2022)
        assert "January 2022" in result
        print("OK === cal(), specific_month mode")
    except Exception as e:
        print(f"ERROR === cal(), specific_month mode\n{e}\n")

# Тестирование ls
def test_ls():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("dir1/", "")
            myzip.writestr("dir1/test_file.txt", "Test content")
        result = ls(["dir1/", "dir1/test_file.txt"])
        assert "dir1/" in result
        assert "test_file.txt" in result
        print("OK === ls(), standard mode")
    except Exception as e:
        print(f"ERROR === ls(), standard mode\n{e}\n")

def test_ls_empty():
    try:
        result = ls([])
        assert "No files or directories found" in result
        print("OK === ls(), empty mode")
    except Exception as e:
        print(f"ERROR === ls(), empty mode\n{e}\n")

# Тестирование cd
def test_cd():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("dir1/", "")
        cur_dir = cd("dir1")[1]
        assert cur_dir == "dir1/"
        print("OK === cd(), standard mode")
    except Exception as e:
        print(f"ERROR === cd(), standard mode\n{e}\n")

def test_cd_invalid_path():
    try:
        msg = cd("non_existing_dir")[0]
        assert "Directory non_existing_dir not found" in msg
        print("OK === cd(), invalid_path mode")
    except Exception as e:
        print(f"ERROR === cd(), invalid_path mode\n{e}\n")

# Тестирование find
def test_find():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("dir1/test_file.txt", "Test content")
        result = find("test_file")
        assert "test_file.txt" in result
        print("OK === find(), standard mode")
    except Exception as e:
        print(f"ERROR === find(), standard mode\n{e}\n")

def test_find_no_results():
    try:
        result = find("non_existing_file")
        assert "No results found" in result
        print("OK === find(), no_results mode")
    except Exception as e:
        print(f"ERROR === find(), no_results mode\n{e}\n")

# Тестирование команды exit
def test_command_exit():
    try:
        command("exit")
    except SystemExit:
        print("OK === command(\"exit\")")
    else:
        print("ERROR === command(\"exit\")")

# Тестирование команды ls
def test_command_ls():
    try:
        with ZipFile(zip_path, "w") as myzip:
            task_1.current_directory = ""
            myzip.writestr("test_file.txt", "Test content")
        result = command("ls")
        assert "test_file.txt" in result
        print("OK === command(\"ls\")")
    except Exception as e:
        print(f"ERROR === command(\"ls\")\n{e}\n")

def test_command_ls_empty():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("dir1/", "")
            task_1.current_directory = "dir/"
        result = command("ls")
        assert "No files or directories found" in result
        print("OK === command(\"ls\")")
    except Exception as e:
        print(f"ERROR === command(\"ls\")\n{e}\n")

# Тестирование команды cd
def test_command_cd():
    try:
        result = command("cd dir1/")[1]
        assert result == "dir1/"
        print("OK === command(\"cd dir1/\")")
    except Exception as e:
        print(f"ERROR === command(\"cd dir1/\")\n{e}\n")

def test_command_cd_invalid():
    try:
        result = command("cd non_existing_dir")[0]
        assert "Directory non_existing_dir not found" in result
        print("OK === command(\"cd non_existing_dir\")")
    except Exception as e:
        print(f"ERROR === command(\"cd non_existing_dir\")\n{e}\n")

# Тестирование команды chmod
def test_command_chmod():
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.writestr("test_file.txt", "Test content")
        command("chmod 755 test_file.txt")
        assert permissions["test_file.txt"] == 0o755
        print("OK === command(\"chmod 755 test_file.txt\")")
    except Exception as e:
        print(f"ERROR === command(\"chmod 755 test_file.txt\")\n{e}\n")

def test_command_chmod_invalid():
    try:
        task_1.current_directory = ""
        result = command("chmod invalid test_file.txt")
        assert "Invalid mode" in result
        print("OK === command(\"chmod invalid test_file.txt\")")
    except Exception as e:
        print(f"ERROR === command(\"chmod invalid test_file.txt\")\n{e}\n")

# Тестирование команды cal
def test_command_cal_current():
    try:
        result = command("cal")
        assert datetime.now().strftime("%B") in result
        print("OK === command(\"cal\")")
    except Exception as e:
        print(f"ERROR === command(\"cal\")\n{e}\n")

def test_command_cal_specific():
    try:
        result = command("cal 1 2022")
        assert "January 2022" in result
        print("OK === command(\"cal 1 2022\")")
    except Exception as e:
        print(f"ERROR === command(\"cal 1 2022\")\n{e}\n")

# Тестирование команды find
def test_command_find():
    try:
        result = command("find test_file")
        assert "test_file.txt" in result
        print("OK === command(\"find test_file\")")
    except Exception as e:
        print(f"ERROR === command(\"find test_file\")\n{e}\n")

def test_command_find_no_results():
    try:
        result = command("find non_existing_file")
        assert "No results found" in result
        print("OK === command(\"find non_existing_file\")")
    except Exception as e:
        print(f"ERROR === command(\"find non_existing_file\")\n{e}\n")


# Запуск всех тестов
def run_tests():
    test_parse_arguments()

    test_chmod()
    test_chmod_invalid_mode()

    test_cal_current_month()
    test_cal_specific_month()

    test_ls()
    test_ls_empty()

    test_cd()
    test_cd_invalid_path()

    test_find()
    test_find_no_results()

    test_command_exit()

    test_command_ls()
    test_command_ls_empty()

    test_command_cd()
    test_command_cd_invalid()

    test_command_chmod()
    test_command_chmod_invalid()

    test_command_cal_current()
    test_command_cal_specific()

    test_command_find()
    test_command_find_no_results()

run_tests()
