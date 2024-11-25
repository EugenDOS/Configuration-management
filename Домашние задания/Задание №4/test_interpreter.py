import pytest
from interpreter import interpreter, popcnt

# Фикстура для создания временных файлов
@pytest.fixture
def create_temp_files(tmp_path):
    binary_path = tmp_path / "program.bin"
    result_path = tmp_path / "result.csv"
    return binary_path, result_path

# Вспомогательная функция для проверки содержимого CSV
def read_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

# Тест: команда load
def test_load_cmd(create_temp_files):
    binary_path, result_path = create_temp_files
    # Бинарный файл с одной командой: load (загрузка 42 в регистр 0)
    binary_data = bytes([0xAD, 0x02, 0x00, 0x00, 0x00])  # load 42 0
    with open(binary_path, "wb") as f:
        f.write(binary_data)
    
    # Запуск интерпретатора
    interpreter(binary_path, result_path, (0, 0))
    
    # Проверка результата
    csv_content = read_csv(result_path)
    assert csv_content == ["Address,Value", "0,0"]  # Память не изменилась, т.к. load влияет только на регистр

# Тест: команда write
def test_write_cmd(create_temp_files):
    binary_path, result_path = create_temp_files
    # Бинарный файл с командами: load 42 в регистр 0, затем write в память по адресу 0
    binary_data = bytes([
        0xAD, 0x02, 0x00, 0x00, 0x00,  # load 42 0
        0x06, 0x00, 0x00, 0x00, 0x00   # write 0 0
    ])
    with open(binary_path, "wb") as f:
        f.write(binary_data)

    # Запуск интерпретатора
    interpreter(binary_path, result_path, (0, 0))

    # Проверка результата
    csv_content = read_csv(result_path)
    assert csv_content == ["Address,Value", "0,42"]  # Проверяем, что значение 42 записалось в память по адресу 0

# Тест: команда read
def test_read_cmd(create_temp_files):
    binary_path, result_path = create_temp_files
    # Бинарный файл с одной командой: read из памяти 0 в регистр 0
    binary_data = bytes([
        0x0E, 0x00, 0x00, 0x00, 0x00   # read 0 0
    ])
    with open(binary_path, "wb") as f:
        f.write(binary_data)

    # Запуск интерпретатора
    interpreter(binary_path, result_path, (0, 0))

    # Проверка результата
    csv_content = read_csv(result_path)
    assert csv_content == ["Address,Value", "0,0"]  # Значение 0 остается, т.к. read изменяет только регистры

# Тест: команда popcnt
def test_popcnt_cmd(create_temp_files):
    binary_path, result_path = create_temp_files
    # Бинарный файл: load 15 в регистр 0, popcnt -> результат в регистр 0
    binary_data = bytes([
        0xFD, 0x00, 0x00, 0x00, 0x00,  # load 15 0
        0x07, 0x00, 0x00, 0x00, 0x00   # popcnt 0 0
    ])
    with open(binary_path, "wb") as f:
        f.write(binary_data)

    # Запуск интерпретатора
    interpreter(binary_path, result_path, (0, 0))

    # Проверка результата
    csv_content = read_csv(result_path)
    assert csv_content == ["Address,Value", "0,0"]  # Значение 0 в памяти, popcnt влияет на регистры

# Тест: несколько команд
def test_several_commands(create_temp_files):
    binary_path, result_path = create_temp_files
    # Программа: load 3, write по адресу 0, load 5, write по адресу 0
    binary_data = bytes([
        0x3D, 0x00, 0x00, 0x00, 0x00,  # load 3 0
        0x06, 0x00, 0x00, 0x00, 0x00,  # write 0 0
        0x5D, 0x00, 0x00, 0x00, 0x00,  # load 5 0
        0x16, 0x00, 0x00, 0x00, 0x00   # write 1 0
    ])
    with open(binary_path, "wb") as f:
        f.write(binary_data)

    # Запуск интерпретатора
    interpreter(binary_path, result_path, (0, 1))

    # Проверка результата
    csv_content = read_csv(result_path)
    assert csv_content == ["Address,Value", "0,3", "1,5"]  # Проверяем, что значения записаны корректно

def test_popcnt():
    assert popcnt(0x29A) == 5
