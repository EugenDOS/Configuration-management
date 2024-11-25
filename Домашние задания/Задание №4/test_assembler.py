from assembler import assembler, serializer, log_operation

# Тестирование функции assembler
def test_load():
    bytes = assembler([("load", 455, 19)])
    assert bytes == [0x7D, 0x1C, 0x00, 0x60, 0x02]

def test_read():
    bytes = assembler([("read", 7, 7)])
    assert bytes == [0x7E, 0x0E, 0x00, 0x00, 0x00]

def test_write():
    bytes = assembler([("write", 590, 10)])
    assert bytes == [0xE6, 0x24, 0x00, 0x00, 0x28]

def test_popcnt():
    bytes = assembler([("popcnt", 26, 0)])
    assert bytes == [0xA7, 0x01, 0x00, 0x00, 0x00]

# Тестирование функции serializer
def test_serializer_load():
    # Пример для команды load (13) с полями B=455, C=19
    cmd = 13
    fields = ((455, 4), (19, 29))
    size = 5
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x7D\x1C\x00\x60\x02'

def test_serializer_read():
    # Пример для команды read (14) с полями B=7, C=7
    cmd = 14
    fields = ((7, 4), (7, 9))
    size = 5
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x7E\x0E\x00\x00\x00'
    
def test_serializer_write():
    # Пример для команды write (6) с полями B=8, C=9
    cmd = 6
    fields = ((8, 4), (9, 34))
    size = 5
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x86\x00\x00\x00\x24'
    
def test_serializer_popcnt():
    # Пример для команды popcnt (7) с полями B=10, C=11
    cmd = 7
    fields = ((10, 4), (11, 9))
    size = 5
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xA7\x16\x00\x00\x00'

# Тестирование логирования операций
def test_log_operation(tmp_path):
    # Временный файл для проверки
    log_file = tmp_path / "log.csv"
    log_operation(log_file, 13, 455, 19)
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert lines[-1] == "A=13,B=455,C=19\n"

# Тестирование комбинации инструкций
def test_multiple_instructions():
    instructions = [
        ("load", 3, 0),
        ("write", 0, 1),
        ("read", 2, 1),
        ("popcnt", 1, 2)
    ]
    bytes = assembler(instructions)
    expected_bytes = [
        0x3D, 0x00, 0x00, 0x00, 0x00,  # load 3 0
        0x06, 0x00, 0x00, 0x00, 0x04,  # write 0 1
        0x2E, 0x02, 0x00, 0x00, 0x00,  # read 2 1
        0x17, 0x04, 0x00, 0x00, 0x00   # popcnt 1 2
    ]
    assert bytes == expected_bytes
