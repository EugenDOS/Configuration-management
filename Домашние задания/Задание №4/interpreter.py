import argparse

def popcnt(value):
    """Подсчет количества установленных битов (единиц) в числе."""
    return bin(value).count('1')

def interpreter(binary_path, result_path, memory_range):
    memory = [0] * 6
    registers = [0]

    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    # Декодирование и исполнение команд
    i = 0
    while i < len(byte_code):
        command = byte_code[i] & 0x0F  # Биты 0-3 для команды
        if command == 13:  # load (Загрузка константы)
            # load <константа (что)> <адрес регистра (куда)>
            B = (int.from_bytes(byte_code[i:i+5], "little") >> 4) & 0x1FFFFFF  # Биты 4-28
            C = (int.from_bytes(byte_code[i:i+5], "little") >> 29) & 0x1F      # Биты 29-33
            registers[C] = B
        elif command == 14:  # read (Чтение из памяти)
            # read <адрес регистра (куда)> <ячейка памяти по адресу, которым явлется значение по адресу регистра (откуда)>
            B = (int.from_bytes(byte_code[i:i+5], "little") >> 4) & 0x1F  # Биты 4-8
            C = (int.from_bytes(byte_code[i:i+5], "little") >> 9) & 0x1F  # Биты 9-13
            registers[B] = memory[registers[C]]
        elif command == 6:  # write (Запись в память)
            # write <адрес ячейки памяти (куда)> <адрес регистра (откуда)>
            B = (int.from_bytes(byte_code[i:i+5], "little") >> 4) & 0x3FFFFFFF  # Биты 4-33
            C = (int.from_bytes(byte_code[i:i+5], "little") >> 34) & 0x1F       # Биты 34-38
            memory[B] = registers[C]
            registers[C] = 0
        elif command == 7:  # popcnt (унарная операция: popcnt(); подсчет количества единиц в числе)
            # popcnt <адрес регистра (куда)> <адрес регистра (откуда)>
            B = (int.from_bytes(byte_code[i:i+5], "little") >> 4) & 0x1F  # Биты 4-8
            C = (int.from_bytes(byte_code[i:i+5], "little") >> 9) & 0x1F  # Биты 9-13
            registers[B] = popcnt(registers[C])
        i += 5  # Переход к следующей команде (каждая команда 5 байт)

    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            result_file.write(f"{address},{memory[address]}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreting the bytes like instructions (from binary file) to the csv-table.")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (csv)")
    parser.add_argument("first_index", help="The first index of the displayed memory")
    parser.add_argument("last_index", help="The last index of the displayed memory")
    args = parser.parse_args()
    interpreter(args.binary_path, args.result_path, (int(args.first_index), int(args.last_index)))
