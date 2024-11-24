import argparse

def log_operation(log_path, operation_code, *args):
    if log_path != None:
        B, C = args
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"A={operation_code},B={B},C={C}\n")

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

def assembler(instructions, log_path=None):
    byte_code = []
    for operation, *args in instructions:
        if operation == "load":
            B, C = args
            byte_code += serializer(13, ((B, 4), (C, 29)), 5)
            log_operation(log_path, 13, B, C)
        elif operation == "read":
            B, C = args
            byte_code += serializer(14, ((B, 4), (C, 9)), 5)
            log_operation(log_path, 14, B, C)
        elif operation == "write":
            B, C = args
            byte_code += serializer(6, ((B, 4), (C, 34)), 5)
            log_operation(log_path, 6, B, C)
        elif operation == "popcnt":
            B, C = args
            byte_code += serializer(7, ((B, 4), (C, 9)), 5)
            log_operation(log_path, 7, B, C)
    return byte_code

def assemble(instructions_path: str, log_path=None):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[j if j.isdigit() == False else int(j) for j in i.split()] for i in f.readlines()]
    return assembler(instructions, log_path)

def save_to_bin(assebled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assebled_instructions))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions file to byte-code.")
    parser.add_argument("instructions_path", help="Path to the instructions file (txt)")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (csv)")
    args = parser.parse_args()
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Operation code,Constant/Address,Address\n")
    result = assemble(args.instructions_path, args.log_path)
    save_to_bin(result, args.binary_path)
    



