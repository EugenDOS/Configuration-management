from assembler import assembler

def test_move():
    bytes = assembler([("load", 455, 19)])
    assert bytes == [0x7D, 0x1C, 0x00, 0x60, 0x02]

def test_read():
    bytes = assembler([("read", 7, 7)])
    assert bytes == [0x7E, 0x0E, 0x00, 0x00, 0x00]

def test_write():
    bytes = assembler([("write", 590, 10)])
    assert bytes == [0xE6, 0x24, 0x00, 0x00, 0x28]

def test_binand():
    bytes = assembler([("popcnt", 26, 0)])
    assert bytes == [0xA7, 0x01, 0x00, 0x00, 0x00]
