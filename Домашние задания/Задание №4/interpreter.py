def popcnt(value):
    """Подсчет количества установленных битов (единиц) в числе."""
    return bin(value).count('1')

def interpreter(binary_path, result_path, memory_range):
    # Задаем память и регистры
    memory = [0] * 6
    registers = [0]

    # Читаем бинарный файл
    with open(binary_path, "rb") as binary_file:
        bytecode = binary_file.read()

    # Декодируем и исполняем команды
    print()
    i = 0
    while i < len(bytecode):
        command = bytecode[i] & 0x0F  # Биты 0-3 для команды
        if command == 13:  # load (Загрузка константы)
            # load <константа (что)> <адрес регистра (куда)>
            B = (int.from_bytes(bytecode[i:i+5], "little") >> 4) & 0x1FFFFFF  # Биты 4-28
            C = (int.from_bytes(bytecode[i:i+5], "little") >> 29) & 0x1F      # Биты 29-33
            print(f"load   | B={B}, C={C}")
            registers[C] = B
        elif command == 14:  # read (Чтение из памяти)
            # read <адрес регистра (куда)> <ячейка памяти по адресу, которым явлется значение по адресу регистра (откуда)>
            B = (int.from_bytes(bytecode[i:i+5], "little") >> 4) & 0x1F  # Биты 4-8
            C = (int.from_bytes(bytecode[i:i+5], "little") >> 9) & 0x1F  # Биты 9-13
            print(f"read   | B={B}, C={C}")
            registers[B] = memory[registers[C]]
        elif command == 6:  # write (Запись в память)
            # write <адрес ячейки памяти (куда)> <адрес регистра (откуда)>
            B = (int.from_bytes(bytecode[i:i+5], "little") >> 4) & 0x3FFFFFFF  # Биты 4-33
            C = (int.from_bytes(bytecode[i:i+5], "little") >> 34) & 0x1F       # Биты 34-38
            print(f"write  | B={B}, C={C}")
            memory[B] = registers[C]
            registers[C] = 0
        elif command == 7:  # popcnt (унарная операция: popcnt(); подсчет количества единиц в числе)
            # popcnt <адрес регистра (куда)> <адрес регистра (откуда)>
            B = (int.from_bytes(bytecode[i:i+5], "little") >> 4) & 0x1F  # Биты 4-8
            C = (int.from_bytes(bytecode[i:i+5], "little") >> 9) & 0x1F  # Биты 9-13
            print(f"popcnt | B={B}, C={C}")
            registers[B] = popcnt(registers[C])
        i += 5  # Переход к следующей команде (каждая команда 5 байт)
    
    print()
    print(f"memory = {memory}")
    print(f"registers = {registers}")
    print()

    # Сохраняем указанный диапазон памяти в файл-результат
    with open(result_path, "w", encoding="utf-8") as csv_file:
        csv_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            csv_file.write(f"{address},{memory[address]}\n")

if __name__ == "__main__":
    interpreter("program.bin", "result.csv", (0, 5))
