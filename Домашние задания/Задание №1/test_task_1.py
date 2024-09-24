import sys, task_1
from task_1 import *
from zipfile import ZipFile

# Независимые тестовые данные
zip_path = "test.zip"
user_name = "test_user"
pc_name = "test_pc"

# Тестирование parse_arguments
def test_parse_arguments():
    sys.argv = ["task_1.py", "test_user", "test_pc", "test.zip"]
    task_1.args = task_1.parse_arguments()
    assert task_1.args.user_name == "test_user"
    assert task_1.args.pc_name == "test_pc"
    assert task_1.args.zip_path == "test.zip"

# Тестирование chmod
def test_chmod():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("test_file.txt", "Test content")
    chmod("755", "test_file.txt")
    assert permissions["test_file.txt"] == 0o755

def test_chmod_invalid_mode():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("test_file.txt", "Test content")
    result = chmod("invalid", "test_file.txt")
    assert "Invalid mode" in result

# Тестирование cal
def test_cal_current_month():
    result = cal()
    current_month = datetime.now().strftime("%B")
    assert current_month in result

def test_cal_specific_month():
    result = cal(1, 2022)
    assert "January 2022" in result

# Тестирование ls
def test_ls():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("dir1/", "")
        myzip.writestr("dir1/test_file.txt", "Test content")
    result = ls(["dir1/", "dir1/test_file.txt"])
    assert "dir1/" in result
    assert "test_file.txt" in result

def test_ls_empty():
    result = ls([])
    assert "No files or directories found" in result

# Тестирование cd
def test_cd():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("dir1/", "")
    cur_dir = cd("dir1")[1]
    lbl = cd("dir1")[2]
    assert cur_dir == "dir1/"
    assert lbl == f"PATH: {task_1.current_directory}"

def test_cd_invalid_path():
    msg = cd("non_existing_dir")[0]
    assert "Directory non_existing_dir not found" in msg

# Тестирование find
def test_find():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("dir1/test_file.txt", "Test content")
    result = find("test_file")
    assert "test_file.txt" in result

def test_find_no_results():
    result = find("non_existing_file")
    assert "No results found" in result

# Тестирование команды ls
def test_command_ls():
    with ZipFile(zip_path, "w") as myzip:
        task_1.current_directory = ""
        myzip.writestr("test_file.txt", "Test content")
    result = command("ls")
    assert "test_file.txt" in result

def test_command_ls_empty():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("dir1/", "")
        task_1.current_directory = "dir/"
    result = command("ls")
    assert "No files or directories found" in result

# Тестирование команды cd
def test_command_cd():
    result = command("cd dir1/")[1]
    lbl = command("cd dir1/")[2]
    assert result == "dir1/"
    assert lbl == f"PATH: {task_1.current_directory}"

def test_command_cd_invalid():
    result = command("cd non_existing_dir")[0]
    assert "Directory non_existing_dir not found" in result

# Тестирование команды chmod
def test_command_chmod():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("test_file.txt", "Test content")
    command("chmod 755 test_file.txt")
    assert permissions["test_file.txt"] == 0o755

def test_command_chmod_invalid():
    task_1.current_directory = ""
    result = command("chmod invalid test_file.txt")
    assert "Invalid mode" in result

# Тестирование команды cal
def test_command_cal_current():
    result = command("cal")
    assert datetime.now().strftime("%B") in result

def test_command_cal_specific():
    result = command("cal 1 2022")
    assert "January 2022" in result

# Тестирование команды find
def test_command_find():
    result = command("find test_file")
    assert "test_file.txt" in result

def test_command_find_no_results():
    result = command("find non_existing_file")
    assert "No results found" in result
